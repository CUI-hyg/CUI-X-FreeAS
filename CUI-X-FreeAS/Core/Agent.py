import Core.MCP_Client as MCPmode
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

class BaseAgent:
    def __init__(self, ConfigPath, userq, UseTools):
        self.ConfigPath = ConfigPath
        self.userq = userq
        self.UseTools = UseTools

    def MCPAgent(self, userq, ConfigPath):
        return MCPmode.AgentMain(userq, ConfigPath)

    def LLMCall(self, userq, ConfigPath):
        try:
            load_dotenv()
            model = os.getenv("MODEL")
            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("BASE_URL"),
            )
            prompt_file = os.path.join(ConfigPath, "Prompt.txt")
            system = ""
            if os.path.exists(prompt_file):
                with open(prompt_file, 'r', encoding='utf-8') as file:
                    system = file.read()
            response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': userq}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            result = response.choices[0].message.content
            return result
        except Exception as e:
            error_msg = f"LLM调用错误: {str(e)}"
            return error_msg

def AgentMain(userq, ConfigPath, UseTools):
    agent = BaseAgent(ConfigPath, userq, UseTools)
    if UseTools == "yes":
        return agent.MCPAgent(userq, ConfigPath)
    else:
        return agent.LLMCall(userq, ConfigPath)
