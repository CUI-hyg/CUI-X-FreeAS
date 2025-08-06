import os
import sys
import json
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(project_root)
import Core.Agent as Agent

class TodoControl:
    def __init__(self, Userq: str):
        self.Userq = Userq

    def create_todo(self):
        configpathl = os.path.abspath(os.path.dirname(__file__))
        data = f"""请根据用户输入,生成todo.md,样例如下:
        [ ] 1.任务内容
        .....(根据实际创建)
        要求:只输出todo.md内容,不输出其他内容
        用户输入:{self.Userq}
        """
        todo = Agent.AgentMain(data, configpathl, "no")
        todo_content = f"""# {self.Userq}

## 任务清单
{todo}
"""
        with open("todo.md", "w", encoding="gbk") as f:
            f.write(todo_content)
        print("todo.md已生成")

    def read_todo(self):
        with open("todo.md", "r", encoding="gbk") as f:
            todo = f.read()
        return todo

    def tick_task(self, task: str):
        todo = self.read_todo()
        todo_lines = todo.splitlines()
        for i, line in enumerate(todo_lines):
            if line.startswith(f"[ ] {task}"):
                todo_lines[i] = f"[√] {task}"
                break
        todo_content = "\n".join(todo_lines)
        with open("todo.md", "w", encoding="gbk") as f:
            f.write(todo_content)
        return f"任务{task}已完成"

class WorkFlowCreator:
    def __init__(self, Userq: str):
        self.Userq = Userq

    def todo2workflow(self, todo_content=None):
        with open(project_root + "\\Env\\Agent_List.txt", "r", encoding="gbk") as f:
            Agents = f.read()
        if todo_content is None:
            with open("todo.md", "r", encoding="gbk") as f:
                todo_content = f.read()
        data = f"""请根据用户输入和任务清单,生成workflow.json,格式如下:
{{
    "workflow_name": "工作流名称",
    "workflow_description": "工作流描述",
    "tasks": [
        {{
            "name": "任务名称1",
            "description": "任务描述1",
            "agent": "XSThinkingAgent"
        }},
        {{
            "name": "任务名称2", 
            "description": "任务描述2",
            "agent": "XSThinkingAgent"
        }}
    ]
}}
        要求:
        1. 只输出JSON内容,不输出其他内容
        2. 根据todo.md中的任务生成对应的tasks数组
        3. 每个任务包含name、description、agent三个字段
        4.可用Agent::{Agents}
        用户输入:{self.Userq}
        任务清单:{todo_content}
        """
        configpathl = os.path.abspath(os.path.dirname(__file__))
        wf = Agent.AgentMain(data, configpathl, "no")
        with open("workflow.json", "w", encoding="gbk") as f:
            f.write(wf)
        return f"workflow.json已生成,{wf}"

    def extract_workflow(self):
        with open("workflow.json", "r", encoding="gbk") as f:
            wf = json.load(f)
        return wf
