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
        process = subprocess.Popen(cmd, env=env)
        process.wait()
        context_path = os.path.join(project_root, 'context.txt')
        if os.path.exists(context_path):
            with open(context_path, 'r', encoding='utf-8') as f:
                result = f.read()
                return result
        else:
            return "任务执行完成,但无回复"
    except Exception as e:
        return f"执行错误: {str(e)}"

@mcp.tool()
def PluginRun(plugin_name: str, plugin_args: str):
    """执行插件,plugin_name:插件名称,plugin_args:插件参数"""
    try:
        cmd = ['python', f'Plugin/Plugin.py', '-n', plugin_name, '-p', plugin_args]
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        process = subprocess.Popen(cmd, env=env)
        process.wait()
        context_path = os.path.join(project_root, 'context.txt')
        if os.path.exists(context_path):
            with open(context_path, 'r', encoding='utf-8') as f:
                result = f.read()
                return result
        else:
            return "插件执行完成，但未有回复"
    except Exception as e:
        return f"执行错误: {str(e)}"

if __name__ == "__main__":
    print("CUIX-FreeMain-MCP 已启动")
    mcp.run(transport='stdio')
