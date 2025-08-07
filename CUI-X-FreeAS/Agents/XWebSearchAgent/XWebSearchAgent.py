import sys
sys.path.append("../../Core/")
import Core.Agent as Agent
import os
import time

def AgentInit(userq, configpath,use_tools):
    try:
        # 使用当前脚本所在目录作为配置路径
        sys.path.append("../Agents/XWebSearchAgent/")
        configpath = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        result = Agent.AgentMain(userq, configpath, "yes")
        if result is None:
            return "任务执行完成，无具体返回结果"
        elif isinstance(result, str):
            return result
        else:
            return str(result)
            
    except Exception as e:
        error_msg = f"Agent执行错误: {str(e)}"
        return error_msg

if __name__ == "__main__":
    print("未启用调试模式")
