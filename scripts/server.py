#!/usr/bin/env python3
"""MCP Automation Server — 21 ferramentas de automação para Claude Code."""

import sys
import os

# Adicionar diretório ao path para imports locais
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import platform

from fastmcp import FastMCP

mcp = FastMCP("automation")

# Registrar ferramentas (Apple/Native apenas em macOS)
from tools.web import register_web_tools
from tools.fs import register_fs_tools
from tools.shell import register_shell_tools

register_web_tools(mcp)
register_fs_tools(mcp)
register_shell_tools(mcp)

if platform.system() == "Darwin":
    from tools.native import register_native_tools
    from tools.apple import register_apple_tools
    register_native_tools(mcp)
    register_apple_tools(mcp)

from tools.snapshot import register_snapshot_tools
register_snapshot_tools(mcp)

if __name__ == "__main__":
    mcp.run()
