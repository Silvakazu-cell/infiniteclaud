import os
from datetime import datetime
from pathlib import Path
from state import state


def web_navigate(url: str) -> str:
    """Navega para uma URL no browser. Abre o browser se ainda não estiver aberto."""
    page = state.get_page()
    page.goto(url, wait_until="domcontentloaded")
    return f"Navegou para: {page.title()} ({url})"


def web_click(selector: str) -> str:
    """Clica em um elemento da página usando CSS selector ou texto visível."""
    page = state.get_page()
    try:
        page.click(selector, timeout=5000)
    except Exception:
        page.get_by_text(selector).first.click(timeout=5000)
    return f"Clicou em: {selector}"


def web_type(selector: str, text: str, clear: bool = True) -> str:
    """Digita texto em um campo de input. Se clear=True, limpa o campo antes."""
    page = state.get_page()
    if clear:
        page.fill(selector, text)
    else:
        page.type(selector, text)
    return f"Digitou '{text[:30]}...' em {selector}"


def web_extract(selector: str, attribute: str = "textContent") -> str:
    """Extrai texto ou atributo de um elemento. Use 'innerHTML' para HTML completo."""
    page = state.get_page()
    element = page.query_selector(selector)
    if not element:
        return f"Elemento não encontrado: {selector}"
    if attribute == "textContent":
        return element.text_content() or ""
    elif attribute == "innerHTML":
        return element.inner_html()
    else:
        return element.get_attribute(attribute) or ""


def web_screenshot(path: str = "") -> str:
    """Tira screenshot da página atual. Se path vazio, salva em screenshots/."""
    page = state.get_page()
    if not path:
        screenshot_dir = os.path.expanduser(
            state.config.get("screenshot_dir", "~/.claude/automation/screenshots")
        )
        Path(screenshot_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(screenshot_dir, f"page_{timestamp}.png")
    page.screenshot(path=path, full_page=True)
    return f"Screenshot salvo em: {path}"


def web_wait(selector: str, timeout: int = 10000) -> str:
    """Aguarda um elemento aparecer na página. Timeout em milissegundos."""
    page = state.get_page()
    page.wait_for_selector(selector, timeout=timeout)
    return f"Elemento encontrado: {selector}"


def web_scroll(direction: str = "down", amount: int = 500) -> str:
    """Rola a página. direction: 'up' ou 'down'. amount: pixels."""
    page = state.get_page()
    delta = amount if direction == "down" else -amount
    page.mouse.wheel(0, delta)
    return f"Rolou {direction} {amount}px"


def web_eval(js_code: str) -> str:
    """Executa JavaScript na página e retorna o resultado."""
    page = state.get_page()
    result = page.evaluate(js_code)
    return str(result)


def register_web_tools(mcp):
    """Registra todas as ferramentas web no servidor MCP."""
    mcp.tool()(web_navigate)
    mcp.tool()(web_click)
    mcp.tool()(web_type)
    mcp.tool()(web_extract)
    mcp.tool()(web_screenshot)
    mcp.tool()(web_wait)
    mcp.tool()(web_scroll)
    mcp.tool()(web_eval)
