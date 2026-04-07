import sys
import os
import json
import glob
from datetime import datetime
from pathlib import Path

# Adicionar o diretório do automation ao path
sys.path.insert(0, os.path.expanduser("~/.claude/automation"))

from tools.web import (web_navigate, web_click, web_type, web_extract,
                        web_screenshot, web_wait, web_scroll, web_eval)
from tools.fs import fs_read, fs_write, fs_list, fs_move, fs_delete
from tools.native import (mouse_click, mouse_move, keyboard_type,
                           keyboard_hotkey, screen_screenshot)
from tools.apple import applescript_run
from tools.shell import shell_run
from state import load_config

CONFIG_PATH = os.path.expanduser("~/.claude/automation/config.json")
LOG_PATH = os.path.expanduser("~/.claude/route-log.jsonl")
SCREENSHOTS_DIR = os.path.expanduser("~/.claude/automation/screenshots")

# Mapa de ferramentas: nome → função
TOOLS_MAP = {
    "web_navigate": web_navigate,
    "web_click": web_click,
    "web_type": web_type,
    "web_extract": web_extract,
    "web_screenshot": web_screenshot,
    "web_wait": web_wait,
    "web_scroll": web_scroll,
    "web_eval": web_eval,
    "fs_read": fs_read,
    "fs_write": fs_write,
    "fs_list": fs_list,
    "fs_move": fs_move,
    "fs_delete": fs_delete,
    "mouse_click": mouse_click,
    "mouse_move": mouse_move,
    "keyboard_type": keyboard_type,
    "keyboard_hotkey": keyboard_hotkey,
    "screen_screenshot": screen_screenshot,
    "applescript_run": applescript_run,
    "shell_run": shell_run,
}

# Descrições das ferramentas por grupo
TOOLS_INFO = {
    "web": [
        {"name": "web_navigate", "params": "url", "desc": "Navega para URL"},
        {"name": "web_click", "params": "selector", "desc": "Clica em elemento"},
        {"name": "web_type", "params": "selector, text", "desc": "Digita em campo"},
        {"name": "web_extract", "params": "selector", "desc": "Extrai texto/HTML"},
        {"name": "web_screenshot", "params": "path?", "desc": "Screenshot da página"},
        {"name": "web_wait", "params": "selector, timeout?", "desc": "Aguarda elemento"},
        {"name": "web_scroll", "params": "direction?, amount?", "desc": "Rola a página"},
        {"name": "web_eval", "params": "js_code", "desc": "Executa JavaScript"},
    ],
    "filesystem": [
        {"name": "fs_read", "params": "path", "desc": "Lê arquivo"},
        {"name": "fs_write", "params": "path, content", "desc": "Escreve arquivo"},
        {"name": "fs_list", "params": "path, recursive?", "desc": "Lista diretório"},
        {"name": "fs_move", "params": "src, dst", "desc": "Move/renomeia"},
        {"name": "fs_delete", "params": "path, confirm", "desc": "Deleta (requer confirm)"},
    ],
    "native": [
        {"name": "mouse_click", "params": "x, y, button?", "desc": "Clica na tela"},
        {"name": "mouse_move", "params": "x, y", "desc": "Move o mouse"},
        {"name": "keyboard_type", "params": "text", "desc": "Digita texto"},
        {"name": "keyboard_hotkey", "params": "keys", "desc": "Atalho de teclado"},
        {"name": "screen_screenshot", "params": "region?", "desc": "Screenshot da tela"},
    ],
    "system": [
        {"name": "applescript_run", "params": "script", "desc": "Executa AppleScript"},
        {"name": "shell_run", "params": "command, timeout?", "desc": "Executa shell command"},
    ],
}

# Histórico de execuções na sessão
execution_history = []


def get_status():
    config = load_config()
    return {
        "status": "active",
        "name": "InfiniteClaud",
        "tools_count": len(TOOLS_MAP),
        "autonomy": config.get("autonomy", "checkpoint"),
        "uptime": datetime.now().isoformat(),
    }


def get_tools():
    return TOOLS_INFO


def run_tool(tool_name: str, args: dict):
    if tool_name not in TOOLS_MAP:
        return {"error": f"Ferramenta não encontrada: {tool_name}", "success": False}

    config = load_config()
    dangerous = config.get("dangerous_actions", [])
    autonomy = config.get("autonomy", "checkpoint")

    if autonomy == "checkpoint" and tool_name in dangerous:
        return {
            "warning": f"Ação destrutiva: {tool_name}. Modo checkpoint ativo.",
            "requires_confirm": True,
            "success": False,
        }

    try:
        fn = TOOLS_MAP[tool_name]
        result = fn(**args)
        entry = {
            "ts": datetime.now().isoformat(),
            "tool": tool_name,
            "args": args,
            "result": str(result)[:500],
            "success": True,
        }
        execution_history.append(entry)
        return {"result": result, "success": True}
    except Exception as e:
        entry = {
            "ts": datetime.now().isoformat(),
            "tool": tool_name,
            "args": args,
            "error": str(e),
            "success": False,
        }
        execution_history.append(entry)
        return {"error": str(e), "success": False}


def get_config():
    return load_config()


def update_config(new_config: dict):
    config = load_config()
    config.update(new_config)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    return config


def get_screenshots():
    Path(SCREENSHOTS_DIR).mkdir(parents=True, exist_ok=True)
    files = sorted(glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png")), reverse=True)
    return [{"path": f, "name": os.path.basename(f)} for f in files[:20]]


def get_logs():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH) as f:
        lines = f.readlines()
    logs = []
    for line in lines[-50:]:
        try:
            logs.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return logs


def get_history():
    return execution_history[-50:]
