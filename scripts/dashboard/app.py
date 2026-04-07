#!/usr/bin/env python3
"""InfiniteClaud Dashboard — Web UI + API REST."""

import sys
import os

# Adicionar diretório do automation ao path
sys.path.insert(0, os.path.expanduser("~/.claude/automation"))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dashboard.api.routes import router

app = FastAPI(title="InfiniteClaud", version="1.0.0")

# Registrar rotas da API
app.include_router(router)

# Servir arquivos estáticos (dashboard UI)
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def dashboard():
    """Serve o dashboard HTML."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/health")
def health():
    return {"status": "ok", "name": "InfiniteClaud Dashboard"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
