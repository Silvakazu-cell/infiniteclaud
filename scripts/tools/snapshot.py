"""MCP tools para Session Snapshot — CRUD de snapshots de sessão."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/automation"))

from snapshot_manager import SnapshotManager

_mgr = SnapshotManager()


def register_snapshot_tools(mcp):
    @mcp.tool()
    async def snapshot_create(description: str, branch: str = "main") -> str:
        """Cria um snapshot da sessão atual com descrição e branch opcionais."""
        snap_id = await _mgr.create_snapshot(description, branch=branch)
        return f"Snapshot criado: {snap_id}"

    @mcp.tool()
    def snapshot_list(branch: str = None) -> list:
        """Lista snapshots disponíveis. Filtra por branch se fornecido."""
        return _mgr.list_snapshots(branch=branch)

    @mcp.tool()
    async def snapshot_restore(snap_id: str) -> dict:
        """Restaura um snapshot pelo ID. Retorna relatório com sucesso, restaurados e avisos."""
        return await _mgr.restore_snapshot(snap_id)

    @mcp.tool()
    async def snapshot_fork(snap_id: str, branch_name: str) -> str:
        """Cria uma nova branch a partir de um snapshot existente (modelo git)."""
        new_id = await _mgr.fork_snapshot(snap_id, branch_name)
        return f"Branch '{branch_name}' criada: {new_id}"

    @mcp.tool()
    async def snapshot_delete(snap_id: str) -> str:
        """Remove permanentemente um snapshot pelo ID."""
        await _mgr.delete_snapshot(snap_id)
        return f"Snapshot {snap_id} removido"
