import json
import time
import os
import sys
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse

sys.path.insert(0, os.path.expanduser("~/.claude/automation"))
from agent_monitor.tracker import get_all_agents, register_agent

agents_router = APIRouter()


@agents_router.get("/api/agents")
def list_agents():
    agents = get_all_agents()
    active = [a for a in agents if a["status"] == "running"]
    recent = [a for a in agents if a["status"] != "running"][-10:]
    total_tokens = sum(a.get("tokens_used", 0) for a in agents)
    return {
        "active": active,
        "recent": recent,
        "summary": {
            "total_tokens": total_tokens,
            "active_count": len(active),
            "completed_count": len([a for a in agents if a["status"] == "completed"]),
        }
    }


@agents_router.get("/api/agents/stream")
def agents_stream():
    def generate():
        while True:
            agents = get_all_agents()
            yield f"data: {json.dumps(agents)}\n\n"
            time.sleep(2)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@agents_router.get("/agents", response_class=HTMLResponse)
def agents_page():
    html_path = os.path.expanduser("~/.claude/automation/dashboard/static/agents.html")
    with open(html_path) as f:
        return f.read()
