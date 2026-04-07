#!/usr/bin/env python3
"""InfiniteClaud Telegram Bot — controle remoto de automações via Telegram."""

import sys
import os
import json
import logging

# Remove '' (CWD) from sys.path to prevent the local telegram/ directory
# from shadowing the installed python-telegram-bot package, then re-add
# the automation root so tools.* imports work correctly.
if '' in sys.path:
    sys.path.remove('')
automation_root = os.path.expanduser("~/.claude/automation")
if automation_root not in sys.path:
    sys.path.append(automation_root)

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes
)

from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tools.fs import fs_read, fs_write, fs_list
from tools.shell import shell_run
from tools.apple import applescript_run
from tools.native import screen_screenshot
from state import load_config
from dashboard.api.assistant import parse_natural_language
from dashboard.api.tasks import TOOLS_MAP

# Importar memory.py usando importlib para evitar conflito com pacote telegram
import importlib.util as _ilu
_mem_spec = _ilu.spec_from_file_location(
    "tg_memory",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.py")
)
_mem_mod = _ilu.module_from_spec(_mem_spec)
_mem_spec.loader.exec_module(_mem_mod)
load_memory = _mem_mod.load_memory
save_memory = _mem_mod.save_memory
learn_pattern = _mem_mod.learn_pattern
find_similar_pattern = _mem_mod.find_similar_pattern
increment_tool_usage = _mem_mod.increment_tool_usage
increment_conversation = _mem_mod.increment_conversation
set_user_name = _mem_mod.set_user_name
get_user_name = _mem_mod.get_user_name
get_stats = _mem_mod.get_stats
register_desired_skill = _mem_mod.register_desired_skill
try_creative_solution = _mem_mod.try_creative_solution
get_desired_skills = _mem_mod.get_desired_skills

# Respostas com personalidade
GREETINGS = ["oi", "olá", "ola", "eai", "e aí", "hey", "hello", "hi", "bom dia", "boa tarde", "boa noite", "fala", "salve"]
THANKS = ["obrigado", "obrigada", "valeu", "thanks", "vlw", "brigado", "brigada"]
STATUS_ASKS = ["como voce está", "como vc está", "como vai", "tudo bem", "status", "como está o servidor", "está funcionando"]
HELP_ASKS = ["o que voce faz", "o que vc faz", "me ajuda", "ajuda", "help", "como funciona", "o que posso fazer"]

# Estado de conversa pendente (aguardando confirmação do usuário)
pending_confirmations = {}

# Config
BOT_CONFIG_PATH = os.path.expanduser("~/.claude/automation/telegram/config.json")
AUTOMATION_CONFIG_PATH = os.path.expanduser("~/.claude/automation/config.json")

logging.basicConfig(
    format="%(asctime)s - InfiniteClaud - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def load_bot_config():
    if os.path.exists(BOT_CONFIG_PATH):
        with open(BOT_CONFIG_PATH) as f:
            return json.load(f)
    return {"token": "", "allowed_users": []}


def is_authorized(update: Update) -> bool:
    """Verifica se o usuário está autorizado."""
    config = load_bot_config()
    allowed = config.get("allowed_users", [])
    if not allowed:
        return True  # Se lista vazia, aceita todos
    return update.effective_user.id in allowed


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Acesso negado.")
        return
    user_first_name = update.effective_user.first_name or "amigo"
    if not get_user_name():
        set_user_name(user_first_name)
    name = get_user_name() or user_first_name
    await update.message.reply_text(
        f"Olá, {name}! 👋 Sou o InfiniteClaud, seu assistente de automação.\n\n"
        f"Me diga o que precisa — posso navegar na web, gerenciar arquivos, "
        f"tirar screenshots, executar comandos e muito mais.\n\n"
        f"Fale naturalmente, tipo: \"tira um screenshot\" ou \"abre o google\".\n\n"
        f"Também aceito comandos:\n"
        f"/status /tools /screenshot /mode /stats",
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    config = load_config()
    await update.message.reply_text(
        f"🟢 *InfiniteClaud Ativo*\n\n"
        f"Ferramentas: 20\n"
        f"Modo: {config.get('autonomy', 'checkpoint')}\n"
        f"Headless: {config.get('browser_headless', False)}\n",
        parse_mode="Markdown",
    )


async def tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    text = (
        "🛠 *Ferramentas InfiniteClaud*\n\n"
        "*Web (Playwright):*\n"
        "web_navigate, web_click, web_type, web_extract, "
        "web_screenshot, web_wait, web_scroll, web_eval\n\n"
        "*Filesystem:*\n"
        "fs_read, fs_write, fs_list, fs_move, fs_delete\n\n"
        "*Nativo macOS:*\n"
        "mouse_click, mouse_move, keyboard_type, "
        "keyboard_hotkey, screen_screenshot\n\n"
        "*Sistema:*\n"
        "applescript_run, shell_run"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text("📸 Tirando screenshot...")
    try:
        result = screen_screenshot()
        # Extrair path do resultado
        path = result.split(": ")[-1].strip()
        if os.path.exists(path):
            with open(path, "rb") as photo:
                await update.message.reply_photo(photo=photo, caption="Screenshot da tela")
        else:
            await update.message.reply_text(f"Screenshot salvo mas não encontrado: {result}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")


async def run_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args:
        await update.message.reply_text("Uso: /run <comando>")
        return
    command = " ".join(context.args)
    await update.message.reply_text(f"⚙️ Executando: `{command}`", parse_mode="Markdown")
    try:
        result = shell_run(command, timeout=30)
        # Truncar resultado se muito longo
        if len(result) > 4000:
            result = result[:4000] + "\n...(truncado)"
        await update.message.reply_text(f"```\n{result}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")


async def files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    path = " ".join(context.args) if context.args else "~"
    try:
        result = fs_list(path)
        if len(result) > 4000:
            result = result[:4000] + "\n...(truncado)"
        await update.message.reply_text(f"📁 `{path}`:\n```\n{result}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")


async def read_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args:
        await update.message.reply_text("Uso: /read <caminho>")
        return
    path = " ".join(context.args)
    try:
        content = fs_read(path)
        if len(content) > 4000:
            content = content[:4000] + "\n...(truncado)"
        await update.message.reply_text(f"📄 `{path}`:\n```\n{content}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")


async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args:
        config = load_config()
        await update.message.reply_text(f"Modo atual: *{config.get('autonomy')}*", parse_mode="Markdown")
        return
    new_mode = context.args[0].lower()
    if new_mode not in ("full", "checkpoint", "plan_first"):
        await update.message.reply_text("Modos: full, checkpoint, plan_first")
        return
    config = load_config()
    config["autonomy"] = new_mode
    with open(AUTOMATION_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    await update.message.reply_text(f"✅ Modo alterado para: *{new_mode}*", parse_mode="Markdown")


async def run_applescript(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args:
        await update.message.reply_text("Uso: /applescript <script>")
        return
    script = " ".join(context.args)
    try:
        result = applescript_run(script)
        await update.message.reply_text(f"🍎 Resultado:\n```\n{result}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")


async def _execute_tool(update: Update, tool_name: str, args: dict, description: str):
    """Executa uma ferramenta e envia o resultado."""
    await update.message.reply_text(f"🔧 {description}...")

    # Screenshot especial — envia como foto
    if tool_name in ("screen_screenshot", "web_screenshot"):
        try:
            fn = TOOLS_MAP[tool_name]
            result = fn(**args)
            path = result.split(": ")[-1].strip()
            if os.path.exists(path):
                with open(path, "rb") as photo:
                    await update.message.reply_photo(photo=photo, caption="✅ Pronto!")
            else:
                await update.message.reply_text(f"✅ {result}")
        except Exception as e:
            await update.message.reply_text(f"❌ Ops, deu erro: {e}")
        return

    # Ferramenta normal
    try:
        fn = TOOLS_MAP[tool_name]
        result = fn(**args)
        result_str = str(result)
        if len(result_str) > 4000:
            result_str = result_str[:4000] + "\n...(truncado)"
        await update.message.reply_text(f"✅ Pronto!\n\n```\n{result_str}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao executar: {e}\n\nTenta de outra forma?")


async def natural_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler conversacional com personalidade e aprendizado."""
    if not is_authorized(update):
        return

    text = update.message.text.strip()
    if not text:
        return

    text_lower = text.lower()
    user_id = update.effective_user.id
    user_first_name = update.effective_user.first_name or "amigo"

    increment_conversation()

    # Salvar nome do usuário na primeira interação
    if not get_user_name():
        set_user_name(user_first_name)

    # --- Saudações ---
    if any(g in text_lower for g in GREETINGS):
        name = get_user_name() or user_first_name
        stats = get_stats()
        if stats["conversations"] < 3:
            await update.message.reply_text(
                f"Olá, {name}! 👋 Sou o InfiniteClaud, seu assistente de automação.\n\n"
                f"Me diga o que precisa — posso navegar na web, gerenciar arquivos, "
                f"tirar screenshots, executar comandos e muito mais.\n\n"
                f"Fale naturalmente, tipo: \"tira um screenshot\" ou \"abre o google\"."
            )
        else:
            await update.message.reply_text(
                f"E aí, {name}! 👋 Pronto pra ajudar. O que precisa?"
            )
        return

    # --- Agradecimentos ---
    if any(t in text_lower for t in THANKS):
        await update.message.reply_text("De nada! 😊 Qualquer coisa, é só chamar.")
        return

    # --- Status / como vai ---
    if any(s in text_lower for s in STATUS_ASKS):
        stats = get_stats()
        config = load_config()
        await update.message.reply_text(
            f"🟢 Tô ativo e funcionando!\n\n"
            f"📊 Já tivemos {stats['conversations']} conversas\n"
            f"✅ {stats['commands_ok']} comandos executados com sucesso\n"
            f"🧠 {stats['patterns_learned']} padrões aprendidos\n"
            f"⚙️ Modo: {config.get('autonomy', 'checkpoint')}\n\n"
            f"Manda ver! 💪"
        )
        return

    # --- Ajuda ---
    if any(h in text_lower for h in HELP_ASKS):
        await update.message.reply_text(
            "Posso fazer várias coisas pelo seu Mac! Alguns exemplos:\n\n"
            "🌐 *Web:* \"navegue para site.com\", \"screenshot da página\"\n"
            "📁 *Arquivos:* \"liste o Desktop\", \"leia o config.json\"\n"
            "🖥 *Sistema:* \"screenshot\", \"execute ls\"\n"
            "🍎 *macOS:* \"applescript tell app...\"\n\n"
            "Fale naturalmente que eu entendo! E se não entender, vou te perguntar 😉",
            parse_mode="Markdown",
        )
        return

    # --- Resposta a confirmação pendente ---
    if user_id in pending_confirmations:
        confirmation = pending_confirmations.pop(user_id)
        if text_lower in ("sim", "s", "yes", "y", "isso", "exato", "confirma"):
            # Aprender o padrão
            learn_pattern(
                confirmation["original_text"],
                confirmation["tool"],
                confirmation["args"]
            )
            # Executar
            await _execute_tool(
                update, confirmation["tool"],
                confirmation["args"],
                confirmation["description"]
            )
        else:
            await update.message.reply_text(
                "Ok, cancelado. Me diz de outra forma o que precisa! 😊"
            )
        return

    # --- Tentar parsear linguagem natural ---
    parsed = parse_natural_language(text)

    if "tool" in parsed:
        # Entendeu! Executar e aprender
        increment_tool_usage(parsed["tool"])
        learn_pattern(text, parsed["tool"], parsed["args"])
        await _execute_tool(
            update, parsed["tool"],
            parsed["args"],
            parsed.get("description", parsed["tool"])
        )
        return

    # --- Não entendeu: buscar padrão similar na memória ---
    similar = find_similar_pattern(text)
    if similar and similar["similarity"] >= 0.7:
        pending_confirmations[user_id] = {
            "original_text": text,
            "tool": similar["tool"],
            "args": similar["args"],
            "description": f"Executar {similar['tool']}",
        }
        await update.message.reply_text(
            f"🤔 Não entendi exatamente, mas parece com algo que já fizemos.\n\n"
            f"Você quis dizer *{similar['tool']}* com `{json.dumps(similar['args'], ensure_ascii=False)}`?\n\n"
            f"Responda *sim* para confirmar ou me explique de outra forma.",
            parse_mode="Markdown",
        )
        return

    # --- Tentar solução criativa combinando ferramentas ---
    creative = try_creative_solution(text)
    if creative:
        await update.message.reply_text(f"💡 {creative['description']}...")
        last_result = None
        for step in creative["steps"]:
            try:
                fn = TOOLS_MAP.get(step["tool"])
                if not fn:
                    continue
                result = fn(**step["args"])
                last_result = result

                # Screenshot → envia como foto
                if step["tool"] in ("screen_screenshot", "web_screenshot"):
                    path = str(result).split(": ")[-1].strip()
                    if os.path.exists(path):
                        with open(path, "rb") as photo:
                            await update.message.reply_photo(photo=photo, caption=f"✅ {step['desc']}")
                        last_result = None
            except Exception as e:
                await update.message.reply_text(f"⚠️ Erro em {step['desc']}: {e}")

        if last_result:
            result_str = str(last_result)
            if len(result_str) > 4000:
                result_str = result_str[:4000] + "\n...(truncado)"
            await update.message.reply_text(f"✅ Pronto!\n\n```\n{result_str}\n```", parse_mode="Markdown")

        # Aprender para próxima vez
        first_step = creative["steps"][0]
        learn_pattern(text, first_step["tool"], first_step["args"])
        increment_tool_usage(first_step["tool"])
        return

    # --- Realmente não sabe: registrar como skill desejada ---
    register_desired_skill(text)
    name = get_user_name() or "amigo"
    await update.message.reply_text(
        f"🧠 {name}, ainda não sei fazer isso, mas já registrei como algo que preciso aprender.\n\n"
        f"Enquanto isso, posso tentar de outra forma? Me explica com outras palavras ou me diz qual ação específica quer.\n\n"
        f"Cada pedido que não entendo me ajuda a evoluir! 💪"
    )


async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    stats = get_stats()
    top = "\n".join([f"  • {t}: {c}x" for t, c in stats["top_tools"]]) if stats["top_tools"] else "  Nenhum ainda"
    desired = stats.get('desired_skills', 0)
    await update.message.reply_text(
        f"🧠 *Meu aprendizado*\n\n"
        f"💬 Conversas: {stats['conversations']}\n"
        f"✅ Comandos OK: {stats['commands_ok']}\n"
        f"📚 Padrões aprendidos: {stats['patterns_learned']}\n"
        f"🎯 Skills que quero aprender: {desired}\n\n"
        f"🔝 Ferramentas mais usadas:\n{top}",
        parse_mode="Markdown",
    )


def main():
    config = load_bot_config()
    token = config.get("token", "")
    if not token:
        print("❌ Token do bot não configurado!")
        print(f"Configure em: {BOT_CONFIG_PATH}")
        print("1. Abra o Telegram e fale com @BotFather")
        print("2. Crie um bot com /newbot")
        print("3. Copie o token e coloque no config.json")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("tools", tools))
    app.add_handler(CommandHandler("screenshot", screenshot))
    app.add_handler(CommandHandler("run", run_cmd))
    app.add_handler(CommandHandler("files", files))
    app.add_handler(CommandHandler("read", read_file))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("applescript", run_applescript))
    app.add_handler(CommandHandler("stats", stats_cmd))

    # Handler para mensagens em linguagem natural (sem /)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, natural_message))

    logger.info("InfiniteClaud Bot iniciado!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
