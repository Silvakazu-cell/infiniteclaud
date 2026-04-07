import re
import os


def parse_natural_language(text: str) -> dict:
    """
    Traduz linguagem natural em chamada de ferramenta.
    Retorna: {"tool": "nome", "args": {}, "description": "o que vai fazer"}
    Ou: {"error": "não entendi"} se não reconhecer.
    """
    text_lower = text.lower().strip()

    # --- WEB: navegação ---
    # "navegue para google.com", "abra https://...", "vá para site.com", "acesse ..."
    url_match = re.search(
        r'(?:navegue?|abra?|va\s+para|acesse|entre\s+(?:no|em|na)?|visite|go\s+to|open)\s+(?:para\s+)?(?:o\s+site\s+)?(?:do\s+|de\s+|da\s+)?(?:https?://)?(\S+)',
        text_lower
    )
    if url_match:
        raw_url = url_match.group(1).strip().rstrip('.,!?')
        if not raw_url.startswith('http'):
            url = f"https://{raw_url}"
        else:
            url = raw_url
        return {
            "tool": "web_navigate",
            "args": {"url": url},
            "description": f"Navegando para {url}"
        }

    # --- WEB: clique ---
    # "clique em #botao", "clique no botão login"
    click_match = re.search(
        r'(?:clique?|click|aperte|pressione)\s+(?:em|no|na|on)?\s*["\']?(.+?)["\']?\s*$',
        text_lower
    )
    if click_match:
        selector = click_match.group(1).strip()
        return {
            "tool": "web_click",
            "args": {"selector": selector},
            "description": f"Clicando em: {selector}"
        }

    # --- WEB: digite ---
    # "digite 'hello' em #input", "escreva 'texto' no campo"
    type_match = re.search(
        r'(?:digite|escreva|type|write)\s+["\'](.+?)["\']\s+(?:em|no|na|in)\s+["\']?(.+?)["\']?\s*$',
        text_lower
    )
    if type_match:
        text_val = type_match.group(1)
        selector = type_match.group(2).strip()
        return {
            "tool": "web_type",
            "args": {"selector": selector, "text": text_val},
            "description": f"Digitando '{text_val}' em {selector}"
        }

    # --- WEB: extrair ---
    # "extraia o texto de .resultado", "pegue o conteúdo de #title"
    extract_match = re.search(
        r'(?:extraia|pegue|capture|get|extract)\s+(?:o\s+)?(?:texto|conteúdo|content|html)\s+(?:de|do|da|from)\s+["\']?(.+?)["\']?\s*$',
        text_lower
    )
    if extract_match:
        selector = extract_match.group(1).strip()
        return {
            "tool": "web_extract",
            "args": {"selector": selector},
            "description": f"Extraindo de: {selector}"
        }

    # --- WEB: screenshot da página ---
    # "screenshot da página", "tire um print da página", "capture a página"
    if re.search(r'(?:screenshot|print|captur[ae])\s+(?:da|de)?\s*(?:página|pagina|page|tela\s+do\s+browser|site)', text_lower):
        return {
            "tool": "web_screenshot",
            "args": {},
            "description": "Tirando screenshot da página"
        }

    # --- NATIVE: screenshot da tela ---
    # "screenshot", "tire um print", "capture a tela", "screenshot da tela"
    if re.search(r'(?:screenshot|print|captur[ae])\s*(?:da)?\s*(?:tela)?|^screenshot$|^print$', text_lower):
        return {
            "tool": "screen_screenshot",
            "args": {},
            "description": "Tirando screenshot da tela"
        }

    # --- SHELL: execute comando ---
    # "execute ls -la", "rode pwd", "run echo hello"
    shell_match = re.search(
        r'(?:execute|rode|run|rodar|executar)\s+(.+)',
        text_lower
    )
    if shell_match:
        command = shell_match.group(1).strip()
        return {
            "tool": "shell_run",
            "args": {"command": command},
            "description": f"Executando: {command}"
        }

    # --- FS: listar ---
    # "liste os arquivos de ~/Desktop", "mostre a pasta Downloads"
    list_match = re.search(
        r'(?:liste|listar|mostre|mostrar|show|ls)\s+(?:os\s+)?(?:arquivos|ficheiros|pasta|diretório|files|folder)\s*(?:de|do|da|em|in|of)?\s*(.+)',
        text_lower
    )
    if list_match:
        path = list_match.group(1).strip().rstrip('.,!?')
        return {
            "tool": "fs_list",
            "args": {"path": path},
            "description": f"Listando: {path}"
        }

    # --- FS: ler arquivo ---
    # "leia o arquivo config.json", "mostre o conteúdo de ~/file.txt"
    read_match = re.search(
        r'(?:leia|ler|read|cat|mostre\s+o\s+conteúdo)\s+(?:o\s+)?(?:arquivo\s+)?(.+)',
        text_lower
    )
    if read_match:
        path = read_match.group(1).strip().rstrip('.,!?')
        return {
            "tool": "fs_read",
            "args": {"path": path},
            "description": f"Lendo: {path}"
        }

    # --- FS: mover ---
    # "mova arquivo.txt para pasta/", "rename old.txt para new.txt"
    move_match = re.search(
        r'(?:mova|mover|move|renomei[ae]|rename)\s+(.+?)\s+(?:para|to|→)\s+(.+)',
        text_lower
    )
    if move_match:
        src = move_match.group(1).strip()
        dst = move_match.group(2).strip()
        return {
            "tool": "fs_move",
            "args": {"src": src, "dst": dst},
            "description": f"Movendo: {src} → {dst}"
        }

    # --- APPLE: applescript ---
    # "applescript tell app ..."
    if text_lower.startswith('applescript ') or text_lower.startswith('osascript '):
        script = text[len('applescript '):].strip() if text_lower.startswith('applescript') else text[len('osascript '):].strip()
        return {
            "tool": "applescript_run",
            "args": {"script": script},
            "description": f"Executando AppleScript"
        }

    # --- NATIVE: mover mouse ---
    mouse_match = re.search(r'(?:mova?\s+o?\s*mouse|cursor)\s+(?:para|to)\s+(\d+)\s*,?\s*(\d+)', text_lower)
    if mouse_match:
        x, y = int(mouse_match.group(1)), int(mouse_match.group(2))
        return {
            "tool": "mouse_move",
            "args": {"x": x, "y": y},
            "description": f"Movendo mouse para ({x}, {y})"
        }

    # --- NATIVE: atalho ---
    hotkey_match = re.search(r'(?:atalho|hotkey|pressione|tecle)\s+(.+)', text_lower)
    if hotkey_match:
        keys = hotkey_match.group(1).strip()
        return {
            "tool": "keyboard_hotkey",
            "args": {"keys": keys},
            "description": f"Atalho: {keys}"
        }

    # --- Não reconhecido ---
    return {
        "error": f"Não entendi o comando. Tente algo como:\n"
                 f"• 'navegue para google.com'\n"
                 f"• 'screenshot'\n"
                 f"• 'execute ls -la'\n"
                 f"• 'liste os arquivos de ~/Desktop'\n"
                 f"• 'leia o arquivo config.json'\n"
                 f"• 'clique em #botao'\n"
                 f"• 'mova arquivo.txt para pasta/'",
        "success": False,
    }
