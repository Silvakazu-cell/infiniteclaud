import subprocess


def applescript_run(script: str) -> str:
    """Executa um script AppleScript e retorna o resultado. Útil para controlar apps macOS nativos."""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return f"Erro AppleScript: {result.stderr.strip()}"
    return result.stdout.strip()


def register_apple_tools(mcp):
    """Registra ferramenta AppleScript no servidor MCP."""
    mcp.tool()(applescript_run)
