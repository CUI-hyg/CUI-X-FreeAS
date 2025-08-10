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
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        process = subprocess.Popen(cmd, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)
        process.wait()
        with open("context.txt", 'r', encoding='utf-8') as f:
                result = f.read()
        return result
    except Exception as e:
        return f"执行错误: {str(e)}"

@mcp.tool()
def PluginRun(plugin_name: str, plugin_args: str):
    """执行插件,plugin_name:插件名称,plugin_args:插件参数"""
    try:
        cmd = ['python', f'Plugin/Plugin.py', '-n', plugin_name, '-p', plugin_args]
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        process = subprocess.Popen(cmd, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)
        process.wait()
        with open("context.txt", 'r', encoding='utf-8') as f:
            result = f.read()
        return result
    except Exception as e:
        return f"执行错误: {str(e)}"

if __name__ == "__main__":
    with open("context.txt", 'w', encoding='utf-8') as f:
        f.write('')
    try:
        if os.path.exists("todo.md"):
            os.remove("todo.md")
        if os.path.exists("workflow.json"):
            os.remove("workflow.json")
    except Exception as e:
        print(f"删除文件时出错: {str(e)}")
    print("CUIX-FreeMain-MCP 已启动")
    mcp.run(transport='stdio')
