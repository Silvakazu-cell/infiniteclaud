#!/bin/bash
# InfiniteClaud — Instalador automático
# Uso: curl -sSL https://raw.githubusercontent.com/douglaskazunari/infiniteclaud/main/setup.sh | bash

set -euo pipefail

echo "⚡ InfiniteClaud — Instalando..."
echo ""

INSTALL_DIR="$HOME/.claude/automation"
PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Criar diretórios
echo "📁 Criando estrutura..."
mkdir -p "$INSTALL_DIR/tools"
mkdir -p "$INSTALL_DIR/router"
mkdir -p "$INSTALL_DIR/dashboard/api"
mkdir -p "$INSTALL_DIR/dashboard/static"
mkdir -p "$INSTALL_DIR/telegram"
mkdir -p "$INSTALL_DIR/tests"
mkdir -p "$INSTALL_DIR/screenshots"

# 2. Copiar scripts
echo "📋 Copiando arquivos..."
cp "$PLUGIN_DIR/scripts/server.py" "$INSTALL_DIR/"
cp "$PLUGIN_DIR/scripts/state.py" "$INSTALL_DIR/"
cp "$PLUGIN_DIR/scripts/config.json" "$INSTALL_DIR/"
cp "$PLUGIN_DIR/scripts/tools/"*.py "$INSTALL_DIR/tools/"
cp "$PLUGIN_DIR/scripts/router/"* "$INSTALL_DIR/router/"
cp "$PLUGIN_DIR/scripts/dashboard/app.py" "$INSTALL_DIR/dashboard/"
cp "$PLUGIN_DIR/scripts/dashboard/api/"*.py "$INSTALL_DIR/dashboard/api/"
cp "$PLUGIN_DIR/scripts/dashboard/static/"* "$INSTALL_DIR/dashboard/static/" 2>/dev/null || true
cp "$PLUGIN_DIR/scripts/telegram/bot.py" "$INSTALL_DIR/telegram/"
cp "$PLUGIN_DIR/scripts/telegram/memory.py" "$INSTALL_DIR/telegram/"

# Criar __init__.py
touch "$INSTALL_DIR/tools/__init__.py"
touch "$INSTALL_DIR/dashboard/__init__.py"
touch "$INSTALL_DIR/dashboard/api/__init__.py"
touch "$INSTALL_DIR/telegram/__init__.py"

# Criar config do telegram se não existir
if [[ ! -f "$INSTALL_DIR/telegram/config.json" ]]; then
  echo '{"token": "", "allowed_users": [], "note": "Configure o token do @BotFather"}' > "$INSTALL_DIR/telegram/config.json"
fi

# 3. Tornar executáveis
chmod +x "$INSTALL_DIR/server.py"
chmod +x "$INSTALL_DIR/router/model_router.sh"
chmod +x "$INSTALL_DIR/dashboard/app.py"
chmod +x "$INSTALL_DIR/telegram/bot.py"

# 4. Instalar dependências Python
echo "📦 Instalando dependências..."
pip3 install fastmcp playwright pyautogui fastapi uvicorn python-telegram-bot 2>/dev/null || {
  echo "⚠️ Algumas dependências falharam. Instale manualmente:"
  echo "   pip3 install fastmcp playwright pyautogui fastapi uvicorn python-telegram-bot"
}

# Instalar browser Playwright se necessário
python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null || {
  echo "📦 Instalando browser Playwright..."
  playwright install chromium 2>/dev/null || true
}

# 5. Registrar MCP server no settings.json
echo "⚙️ Registrando no Claude Code..."
SETTINGS="$HOME/.claude/settings.json"
if [[ -f "$SETTINGS" ]]; then
  # Adicionar mcpServers.automation
  tmp=$(mktemp)
  jq --arg path "$INSTALL_DIR/server.py" '.mcpServers.automation = {"command": "python3", "args": [$path]}' "$SETTINGS" > "$tmp" && mv "$tmp" "$SETTINGS"

  # Adicionar hook do Model Router
  jq '.hooks.UserPromptSubmit = [{"hooks": [{"type": "command", "command": "bash ~/.claude/automation/router/model_router.sh", "statusMessage": "⚡ InfiniteClaud Router..."}]}]' "$SETTINGS" > "$tmp" && mv "$tmp" "$SETTINGS"
else
  echo "⚠️ settings.json não encontrado. Configure manualmente."
fi

echo ""
echo "✅ InfiniteClaud instalado com sucesso!"
echo ""
echo "   🔧 20 ferramentas MCP ativas"
echo "   ⚡ Model Router (Haiku/Sonnet/Opus)"
echo "   🌐 Dashboard: python3 ~/.claude/automation/dashboard/app.py"
echo "   📱 Telegram:  python3 ~/.claude/automation/telegram/bot.py"
echo ""
echo "   Ative no Claude Code com: /InfiniteClaud"
echo ""
