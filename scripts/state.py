import json
import os
from pathlib import Path
from typing import Optional

CONFIG_PATH = Path(os.path.expanduser("~/.claude/automation/config.json"))


def load_config() -> dict:
    """Carrega configuração de autonomia."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {
        "autonomy": "checkpoint",
        "dangerous_actions": ["fs_delete", "shell_run", "keyboard_hotkey"],
        "require_confirm_for_dangerous": True,
        "browser_headless": False,
        "screenshot_dir": "~/.claude/automation/screenshots",
    }


class AppState:
    """Estado global compartilhado entre todas as ferramentas."""

    def __init__(self):
        self.playwright_instance = None
        self.browser = None
        self.context = None  # BrowserContext para persistência de sessão
        self.page = None
        self.config = load_config()

    def get_page(self):
        """Retorna a página ativa, inicializando browser se necessário."""
        if not self.playwright_instance:
            from playwright.sync_api import sync_playwright
            self.playwright_instance = sync_playwright().start()
            headless = self.config.get("browser_headless", False)
            self.browser = self.playwright_instance.chromium.launch(headless=headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
        return self.page

    def new_page(self):
        """Abre nova aba no contexto atual."""
        if not self.browser:
            self.get_page()
        if not self.context:
            self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return self.page

    async def capture_browser_state(self) -> dict:
        """Captura estado atual do browser: URL, cookies, localStorage, scroll.

        Retorna {} se o browser não estiver inicializado.
        """
        if not self.page or not self.context:
            return {}

        try:
            url = self.page.url
            cookies = self.context.cookies()
            scroll_position = self.page.evaluate(
                "() => ({ x: window.scrollX, y: window.scrollY })"
            )
            local_storage = self.page.evaluate(
                "() => { const s = {}; for (let i = 0; i < localStorage.length; i++) { "
                "const k = localStorage.key(i); s[k] = localStorage.getItem(k); } return s; }"
            )
            return {
                "url": url,
                "cookies": cookies,
                "local_storage": local_storage,
                "scroll_position": scroll_position,
            }
        except Exception:
            return {}

    def shutdown(self):
        """Fecha browser e Playwright."""
        if self.context:
            self.context.close()
            self.context = None
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright_instance:
            self.playwright_instance.stop()
            self.playwright_instance = None
        self.page = None


# Instância global
state = AppState()
