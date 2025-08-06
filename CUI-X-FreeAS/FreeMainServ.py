import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
import subprocess

mcp = FastMCP()

@mcp.tool()
def AgentRun(userq: str):
    """执行AgentGroup任务,userq:用户完整的问题"""
    try:
        cmd = ['python', 'FreeLoopAPI.py', '--query', userq]
        process = subprocess.Popen(cmd,creationflags=subprocess.CREATE_NEW_CONSOLE)
        process.wait()
        with open('context.txt', 'r', encoding='utf-8') as f:
            result = f.read()
            return result
    except Exception as e:
        return f"执行错误: {str(e)}"
if __name__ == "__main__":
    print("CUIX-FreeMain-MCP 已启动")
    mcp.run(transport='stdio')
