import os
import shutil
from pathlib import Path


def fs_read(path: str) -> str:
    """Lê e retorna o conteúdo de um arquivo."""
    expanded = os.path.expanduser(path)
    if not os.path.exists(expanded):
        return f"Arquivo não encontrado: {path}"
    with open(expanded, "r") as f:
        return f.read()


def fs_write(path: str, content: str) -> str:
    """Escreve conteúdo em um arquivo. Cria diretórios intermediários se necessário."""
    expanded = os.path.expanduser(path)
    Path(expanded).parent.mkdir(parents=True, exist_ok=True)
    with open(expanded, "w") as f:
        f.write(content)
    return f"Escrito {len(content)} bytes em: {path}"


def fs_list(path: str, recursive: bool = False) -> str:
    """Lista arquivos e diretórios. Se recursive=True, lista subdiretórios."""
    expanded = os.path.expanduser(path)
    if not os.path.exists(expanded):
        return f"Diretório não encontrado: {path}"
    entries = []
    if recursive:
        for root, dirs, files in os.walk(expanded):
            for name in dirs + files:
                rel = os.path.relpath(os.path.join(root, name), expanded)
                entries.append(rel)
    else:
        entries = os.listdir(expanded)
    return "\n".join(sorted(entries))


def fs_move(src: str, dst: str) -> str:
    """Move ou renomeia um arquivo/diretório."""
    src_exp = os.path.expanduser(src)
    dst_exp = os.path.expanduser(dst)
    if not os.path.exists(src_exp):
        return f"Origem não encontrada: {src}"
    Path(dst_exp).parent.mkdir(parents=True, exist_ok=True)
    shutil.move(src_exp, dst_exp)
    return f"Movido: {src} → {dst}"


def fs_delete(path: str, confirm: bool = False) -> str:
    """Deleta arquivo ou diretório. Requer confirm=True como segurança."""
    if not confirm:
        return "Ação destrutiva. Requer confirm=True para executar."
    expanded = os.path.expanduser(path)
    if not os.path.exists(expanded):
        return f"Não encontrado: {path}"
    if os.path.isdir(expanded):
        shutil.rmtree(expanded)
    else:
        os.remove(expanded)
    return f"Deletado: {path}"


def register_fs_tools(mcp):
    """Registra ferramentas de filesystem no servidor MCP."""
    mcp.tool()(fs_read)
    mcp.tool()(fs_write)
    mcp.tool()(fs_list)
    mcp.tool()(fs_move)
    mcp.tool()(fs_delete)
