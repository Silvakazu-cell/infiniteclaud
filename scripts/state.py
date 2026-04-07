import json
import os
from pathlib import Path

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
        self.page = None
        self.config = load_config()

    def get_page(self):
        """Retorna a página ativa, inicializando browser se necessário."""
        if not self.playwright_instance:
            from playwright.sync_api import sync_playwright
            self.playwright_instance = sync_playwright().start()
            headless = self.config.get("browser_headless", False)
            self.browser = self.playwright_instance.chromium.launch(headless=headless)
            self.page = self.browser.new_page()
        return self.page

    def new_page(self):
        """Abre nova aba."""
        if not self.browser:
            self.get_page()
        self.page = self.browser.new_page()
        return self.page

    def shutdown(self):
        """Fecha browser e Playwright."""
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright_instance:
            self.playwright_instance.stop()
            self.playwright_instance = None
        self.page = None


# Instância global
state = AppState()
