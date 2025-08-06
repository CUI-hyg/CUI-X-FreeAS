import sys
sys.path.append("../../Framework/GUIOperator/")
from Framework.GUIOperator import GUIOperator
import os

def AgentInit(userq,configpath,use_tool):
    try:
        import asyncio
        agent_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(GUIOperator.Run("yes", userq, agent_dir))
        return result
    except Exception as e:
        error_msg = f"Agent执行错误: {str(e)}"
        return error_msg

if __name__ == "__main__":
    print("你未开启调试模式")