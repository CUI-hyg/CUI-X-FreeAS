import sys
sys.path.append("../../Core/")
import Core.Agent as Agent
import os

def AgentInit(userq,configpath):
    try:
        # 使用当前脚本所在目录作为配置路径
        agent_dir = os.path.dirname(os.path.abspath(__file__))
        result = Agent.AgentMain(userq, agent_dir, "yes")
        
        # 统一处理返回值
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
    #userq = input("请输入你的问题:")
    #AgentInit(userq,"yes")
    #若你希望调试这个Agent,解除上面的注释
    print("你未开启调试模式")