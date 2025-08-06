import sys
sys.path.append("../../Core/")
from Core import Agent
import os

def AgentInit(userq,configpath,use_tool):
    try:
        # 使用当前脚本所在目录作为配置路径
        agent_dir = os.path.dirname(os.path.abspath(__file__))
        result = Agent.AgentMain(userq, configpath, use_tool)
        return str(result)
    except Exception as e:
        error_msg = f"Agent执行错误: {str(e)}"
        return error_msg

if __name__ == "__main__":
    print("未开启调试模式")