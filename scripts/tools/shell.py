import subprocess


def shell_run(command: str, timeout: int = 30) -> str:
    """Executa um comando shell e retorna stdout, stderr e exit code."""
    result = subprocess.run(
        command, shell=True,
        capture_output=True, text=True, timeout=timeout
    )
    output = ""
    if result.stdout:
        output += f"stdout:\n{result.stdout}\n"
    if result.stderr:
        output += f"stderr:\n{result.stderr}\n"
    output += f"exit_code: {result.returncode}"
    return output


def register_shell_tools(mcp):
    """Registra ferramentas de shell no servidor MCP."""
    mcp.tool()(shell_run)
