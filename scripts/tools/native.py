import os
from datetime import datetime
from pathlib import Path
import pyautogui

pyautogui.FAILSAFE = True


def mouse_click(x: int, y: int, button: str = "left") -> str:
    """Clica em uma coordenada da tela. button: 'left', 'right', 'middle'."""
    pyautogui.click(x=x, y=y, button=button)
    return f"Clicou em ({x}, {y}) botão {button}"


def mouse_move(x: int, y: int) -> str:
    """Move o cursor do mouse para uma coordenada da tela."""
    pyautogui.moveTo(x=x, y=y, duration=0.3)
    return f"Mouse movido para ({x}, {y})"


def keyboard_type(text: str) -> str:
    """Digita texto globalmente (onde o cursor estiver focado)."""
    pyautogui.write(text, interval=0.02)
    return f"Digitou: '{text[:50]}...'" if len(text) > 50 else f"Digitou: '{text}'"


def keyboard_hotkey(keys: str) -> str:
    """Executa atalho de teclado. Formato: 'cmd+c', 'ctrl+shift+n', 'alt+tab'."""
    import platform as _plat
    is_mac = _plat.system() == "Darwin"

    key_list = [k.strip() for k in keys.split("+")]
    mapped = []
    for k in key_list:
        k_lower = k.lower()
        if k_lower == "cmd":
            mapped.append("command" if is_mac else "win")
        elif k_lower == "ctrl":
            mapped.append("ctrl")
        elif k_lower == "alt":
            mapped.append("option" if is_mac else "alt")
        elif k_lower == "shift":
            mapped.append("shift")
        else:
            mapped.append(k_lower)
    pyautogui.hotkey(*mapped)
    return f"Executou atalho: {keys}"


def screen_screenshot(region: str = "") -> str:
    """Tira screenshot da tela inteira ou de uma região (formato: 'x,y,w,h')."""
    screenshot_dir = os.path.expanduser("~/.claude/automation/screenshots")
    Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshot_dir, f"screen_{timestamp}.png")

    if region:
        parts = [int(p.strip()) for p in region.split(",")]
        x, y, w, h = parts[0], parts[1], parts[2], parts[3]
        img = pyautogui.screenshot(region=(x, y, w, h))
    else:
        img = pyautogui.screenshot()
    img.save(path)
    return f"Screenshot da tela salvo em: {path}"


def register_native_tools(mcp):
    """Registra ferramentas nativas macOS (PyAutoGUI) no servidor MCP."""
    mcp.tool()(mouse_click)
    mcp.tool()(mouse_move)
    mcp.tool()(keyboard_type)
    mcp.tool()(keyboard_hotkey)
    mcp.tool()(screen_screenshot)
