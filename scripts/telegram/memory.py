import json
import os
from datetime import datetime
from difflib import SequenceMatcher

MEMORY_PATH = os.path.expanduser("~/.claude/automation/telegram/user_memory.json")


def load_memory() -> dict:
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH) as f:
            return json.load(f)
    return {
        "learned_patterns": {},  # "frase do usuario" → {"tool": "x", "args": {}}
        "user_preferences": {},  # preferências aprendidas
        "conversation_count": 0,
        "successful_commands": 0,
        "last_interaction": None,
        "frequently_used": {},  # tool → count
        "user_name": None,
    }


def save_memory(memory: dict):
    memory["last_interaction"] = datetime.now().isoformat()
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def learn_pattern(user_text: str, tool: str, args: dict):
    """Aprende uma associação entre texto do usuário e ferramenta."""
    memory = load_memory()
    key = user_text.lower().strip()
    memory["learned_patterns"][key] = {
        "tool": tool,
        "args": args,
        "learned_at": datetime.now().isoformat(),
        "use_count": 0,
    }
    save_memory(memory)


def find_similar_pattern(text: str, threshold: float = 0.6) -> dict | None:
    """Busca padrões similares na memória usando fuzzy matching."""
    memory = load_memory()
    text_lower = text.lower().strip()

    best_match = None
    best_score = 0.0

    for pattern, data in memory.get("learned_patterns", {}).items():
        score = SequenceMatcher(None, text_lower, pattern).ratio()
        if score > best_score and score >= threshold:
            best_score = score
            best_match = {**data, "original_pattern": pattern, "similarity": score}

    return best_match


def increment_tool_usage(tool: str):
    memory = load_memory()
    memory["successful_commands"] = memory.get("successful_commands", 0) + 1
    memory["conversation_count"] = memory.get("conversation_count", 0) + 1
    freq = memory.get("frequently_used", {})
    freq[tool] = freq.get(tool, 0) + 1
    memory["frequently_used"] = freq
    save_memory(memory)


def increment_conversation():
    memory = load_memory()
    memory["conversation_count"] = memory.get("conversation_count", 0) + 1
    save_memory(memory)


def set_user_name(name: str):
    memory = load_memory()
    memory["user_name"] = name
    save_memory(memory)


def get_user_name() -> str | None:
    return load_memory().get("user_name")


def register_desired_skill(user_text: str, context: str = ""):
    """Registra algo que o usuário pediu mas o bot não soube fazer.
    Serve como backlog de evolução — o bot 'sabe' o que não sabe."""
    memory = load_memory()
    if "desired_skills" not in memory:
        memory["desired_skills"] = []
    memory["desired_skills"].append({
        "request": user_text,
        "context": context,
        "registered_at": datetime.now().isoformat(),
        "resolved": False,
    })
    # Manter apenas os últimos 100
    memory["desired_skills"] = memory["desired_skills"][-100:]
    save_memory(memory)


def get_desired_skills() -> list:
    memory = load_memory()
    return [s for s in memory.get("desired_skills", []) if not s.get("resolved")]


def resolve_desired_skill(request_text: str):
    """Marca uma skill desejada como resolvida (o bot aprendeu)."""
    memory = load_memory()
    for skill in memory.get("desired_skills", []):
        if skill["request"].lower() == request_text.lower():
            skill["resolved"] = True
            skill["resolved_at"] = datetime.now().isoformat()
    save_memory(memory)


def try_creative_solution(text: str) -> dict | None:
    """Tenta resolver um pedido desconhecido combinando ferramentas existentes.
    Analisa palavras-chave para montar uma sequência criativa."""
    text_lower = text.lower()

    # Busca por URL ou site mencionado
    import re
    url_in_text = re.search(r'(https?://\S+|[\w.-]+\.(com|net|org|io|ai|dev|br)\S*)', text_lower)

    # Se menciona algo sobre web/site/página + alguma ação
    if url_in_text:
        url = url_in_text.group(1)
        if not url.startswith('http'):
            url = f"https://{url}"

        # Quer informação de um site → navegar + extrair
        if any(w in text_lower for w in ['informação', 'informacao', 'conteúdo', 'conteudo', 'dados', 'pesquise', 'pesquisar', 'busque', 'buscar', 'procure', 'procurar', 'traga', 'trazer', 'mostre', 'mostrar', 'veja', 'ver', 'encontre', 'encontrar', 'solução', 'solucao', 'preço', 'preco', 'como']):
            return {
                "steps": [
                    {"tool": "web_navigate", "args": {"url": url}, "desc": f"Abrindo {url}"},
                    {"tool": "web_extract", "args": {"selector": "body"}, "desc": "Extraindo conteúdo"},
                ],
                "description": f"Vou navegar até {url} e extrair o conteúdo pra você",
                "creative": True,
            }
        # Quer screenshot de um site
        if any(w in text_lower for w in ['screenshot', 'print', 'captura', 'imagem', 'foto', 'visual']):
            return {
                "steps": [
                    {"tool": "web_navigate", "args": {"url": url}, "desc": f"Abrindo {url}"},
                    {"tool": "web_screenshot", "args": {}, "desc": "Tirando screenshot"},
                ],
                "description": f"Vou abrir {url} e tirar um screenshot",
                "creative": True,
            }

    # Pesquisar no Google
    if any(w in text_lower for w in ['pesquise', 'pesquisar', 'busque', 'buscar', 'procure', 'procurar', 'google', 'search']):
        # Extrair o termo de busca
        for prefix in ['pesquise ', 'pesquisar ', 'busque ', 'buscar ', 'procure ', 'procurar ', 'pesquise sobre ', 'busque sobre ', 'procure sobre ']:
            if prefix in text_lower:
                query = text_lower.split(prefix, 1)[1].strip()
                return {
                    "steps": [
                        {"tool": "web_navigate", "args": {"url": f"https://www.google.com/search?q={query}"}, "desc": f"Pesquisando '{query}' no Google"},
                        {"tool": "web_extract", "args": {"selector": "body"}, "desc": "Extraindo resultados"},
                    ],
                    "description": f"Vou pesquisar '{query}' no Google e trazer os resultados",
                    "creative": True,
                }

    # Informações do sistema
    if any(w in text_lower for w in ['bateria', 'espaço disco', 'espaco disco', 'memória', 'memoria', 'cpu', 'processos', 'rede', 'wifi', 'ip']):
        if 'bateria' in text_lower:
            return {"steps": [{"tool": "shell_run", "args": {"command": "pmset -g batt"}, "desc": "Verificando bateria"}], "description": "Verificando nível de bateria", "creative": True}
        if any(w in text_lower for w in ['espaço disco', 'espaco disco', 'armazenamento', 'storage']):
            return {"steps": [{"tool": "shell_run", "args": {"command": "df -h /"}, "desc": "Verificando disco"}], "description": "Verificando espaço em disco", "creative": True}
        if any(w in text_lower for w in ['memória', 'memoria', 'ram']):
            return {"steps": [{"tool": "shell_run", "args": {"command": "vm_stat | head -5"}, "desc": "Verificando memória"}], "description": "Verificando uso de memória", "creative": True}
        if any(w in text_lower for w in ['ip', 'rede', 'wifi', 'internet']):
            return {"steps": [{"tool": "shell_run", "args": {"command": "ifconfig en0 | grep inet"}, "desc": "Verificando rede"}], "description": "Verificando informações de rede", "creative": True}
        if any(w in text_lower for w in ['cpu', 'processos', 'processo']):
            return {"steps": [{"tool": "shell_run", "args": {"command": "top -l 1 -n 5 | head -15"}, "desc": "Verificando processos"}], "description": "Verificando processos ativos", "creative": True}

    # Abrir app nativo — mapeia nomes comuns para apps reais
    import re as _re
    app_map = {
        'terminal': 'Terminal', 'finder': 'Finder', 'safari': 'Safari',
        'chrome': 'Google Chrome', 'spotify': 'Spotify', 'music': 'Music',
        'musica': 'Music', 'notas': 'Notes', 'notes': 'Notes',
        'calculadora': 'Calculator', 'calculator': 'Calculator',
        'mail': 'Mail', 'email': 'Mail', 'messages': 'Messages',
        'mensagens': 'Messages', 'calendar': 'Calendar', 'calendario': 'Calendar',
        'photos': 'Photos', 'fotos': 'Photos', 'preview': 'Preview',
        'textedit': 'TextEdit', 'vscode': 'Visual Studio Code',
        'code': 'Visual Studio Code', 'slack': 'Slack', 'discord': 'Discord',
        'telegram': 'Telegram', 'whatsapp': 'WhatsApp', 'notion': 'Notion',
        'keynote': 'Keynote', 'pages': 'Pages', 'numbers': 'Numbers',
        'xcode': 'Xcode', 'iterm': 'iTerm', 'iterm2': 'iTerm',
    }

    open_match = _re.search(
        r'(?:abr[ae]|abrir|open)\s+(?:o|a|um[a]?\s+(?:nova?\s+)?(?:aba|janela)\s+(?:do|da|de|no|na)\s+)?(\w+)',
        text_lower
    )
    if open_match:
        raw_app = open_match.group(1).strip()
        app_name = app_map.get(raw_app, raw_app.capitalize())
        # Para "nova aba do terminal" → abrir nova janela do Terminal
        if 'nova aba' in text_lower or 'nova janela' in text_lower:
            script = f'tell application "{app_name}" to activate\ntell application "System Events" to keystroke "t" using command down'
            desc = f"Abrindo nova aba no {app_name}"
        else:
            script = f'tell application "{app_name}" to activate'
            desc = f"Abrindo {app_name}"
        return {
            "steps": [{"tool": "applescript_run", "args": {"script": script}, "desc": desc}],
            "description": desc,
            "creative": True,
        }

    # Hora / data
    if any(w in text_lower for w in ['que horas', 'hora atual', 'que dia', 'data atual', 'data de hoje']):
        return {"steps": [{"tool": "shell_run", "args": {"command": "date"}, "desc": "Verificando data/hora"}], "description": "Verificando data e hora", "creative": True}

    # Clima / tempo — mais restritivo para não confundir "tempo" (time) com weather
    if any(w in text_lower for w in ['clima', 'temperatura', 'previsão do tempo', 'previsao do tempo', 'weather', 'graus', 'chover', 'chuva', 'sol hoje', 'tempo hoje', 'tempo agora']):
        return {
            "steps": [
                {"tool": "shell_run", "args": {"command": "curl -s 'wttr.in/?format=3' 2>/dev/null || echo 'Sem acesso ao serviço de clima'"}, "desc": "Buscando clima"},
            ],
            "description": "Vou buscar o clima atual",
            "creative": True,
        }

    return None


def get_stats() -> dict:
    memory = load_memory()
    return {
        "conversations": memory.get("conversation_count", 0),
        "commands_ok": memory.get("successful_commands", 0),
        "patterns_learned": len(memory.get("learned_patterns", {})),
        "desired_skills": len([s for s in memory.get("desired_skills", []) if not s.get("resolved")]),
        "top_tools": sorted(
            memory.get("frequently_used", {}).items(),
            key=lambda x: x[1], reverse=True
        )[:5],
    }
