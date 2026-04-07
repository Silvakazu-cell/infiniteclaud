from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.expanduser("~/.claude/automation"))

from dashboard.api.tasks import (
    get_status, get_tools, run_tool, get_config,
    update_config, get_screenshots, get_logs, get_history
)
from dashboard.api.assistant import parse_natural_language

router = APIRouter(prefix="/api")


class RunRequest(BaseModel):
    tool: str
    args: dict = {}
    force: bool = False


class ConfigUpdate(BaseModel):
    autonomy: Optional[str] = None
    browser_headless: Optional[bool] = None


class AssistantRequest(BaseModel):
    text: str


@router.get("/status")
def api_status():
    return get_status()


@router.get("/tools")
def api_tools():
    return get_tools()


@router.post("/run")
def api_run(req: RunRequest):
    if req.force:
        from dashboard.api.tasks import TOOLS_MAP
        if req.tool not in TOOLS_MAP:
            raise HTTPException(404, f"Ferramenta não encontrada: {req.tool}")
        try:
            fn = TOOLS_MAP[req.tool]
            result = fn(**req.args)
            return {"result": result, "success": True}
        except Exception as e:
            raise HTTPException(500, str(e))
    return run_tool(req.tool, req.args)


@router.get("/config")
def api_config():
    return get_config()


@router.put("/config")
def api_update_config(update: ConfigUpdate):
    changes = {k: v for k, v in update.dict().items() if v is not None}
    if not changes:
        raise HTTPException(400, "Nenhum campo para atualizar")
    return update_config(changes)


@router.get("/screenshots")
def api_screenshots():
    return get_screenshots()


@router.get("/logs")
def api_logs():
    return get_logs()


@router.get("/history")
def api_history():
    return get_history()


@router.post("/assistant")
def api_assistant(req: AssistantRequest):
    parsed = parse_natural_language(req.text)
    if "error" in parsed:
        return parsed
    # Executar a ferramenta parseada
    result = run_tool(parsed["tool"], parsed["args"])
    return {
        "parsed": parsed,
        "result": result,
    }
