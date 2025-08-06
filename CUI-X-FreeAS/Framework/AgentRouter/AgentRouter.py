import os
import sys
import json
import asyncio
import uuid
import importlib.util
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

class AgentRouter:
    def __init__(self, agent_name: str,userq:str,agent_use_tool:str):
        self.agent_name = agent_name
        self.agent_path = os.path.join(project_root, "Agents", self.agent_name, f"{self.agent_name}.py")
        self.userq = userq
        self.agent_use_tool = agent_use_tool

    def get_all_agents(self):
        agents_dir = os.path.join(project_root, "Agents")
        agents = []
        if os.path.isdir(agents_dir):
            for agent_name in os.listdir(agents_dir):
                agent_json_path = os.path.join(agents_dir, agent_name, "Agent.json")
                if os.path.isfile(agent_json_path):
                    agent_path = os.path.join(agents_dir, agent_name, f"{agent_name}.py")
                    agents.append({
                        "name": agent_name,
                        "path": agent_path
                    })
        return agents

    def load_agent(self):
        possible_paths = [
            os.path.join(project_root, "Agents", self.agent_name, f"{self.agent_name}.py"),
            os.path.join(project_root, "Agents", self.agent_name, f"{self.agent_name[:-5]}.py"),
            os.path.join(project_root, "Agents", self.agent_name, f"{self.agent_name}.py"),
        ]
        agent_path = None
        for path in possible_paths:
            if os.path.isfile(path):
                agent_path = path
                break
        if not agent_path:
            return f"不存在该Agent:{self.agent_name}"
        spec = importlib.util.spec_from_file_location(self.agent_name, agent_path)
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        return agent_module

    def run_agent(self):
        Config_Path = os.path.join(project_root, "Agents", self.agent_name)
        Agent = self.load_agent()
        if isinstance(Agent, str):
            return Agent
        try:
            answer = Agent.AgentInit(self.userq, Config_Path, self.agent_use_tool)
        except TypeError as e:
            answer = f"Agent参数错误: {str(e)}"
        except Exception as e:
            answer = f"Agent执行错误: {str(e)}"
        return answer

    def main_loop(self):
        answer = self.run_agent()
        return answer

def Agent_Router(agent_name: str,userq:str,agent_use_tool:str):
    agent_router = AgentRouter(agent_name,userq,agent_use_tool)
    answer = agent_router.main_loop()
    return answer