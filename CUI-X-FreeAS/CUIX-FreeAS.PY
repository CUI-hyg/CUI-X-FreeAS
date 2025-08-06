import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from Core import Agent

class CUIXFreeAS:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__)) + "/Env"
        
    def welcome(self):
        welcome = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    CUI X-FreeAS - 下一代Agent系统 - AlphaV4                  ║
║                                                                              ║
║                  Version 0.5.76-R6 - 2025.08.06-BuildD6                      ║  
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(welcome)
        
    def display_help(self):
        help_text = """
可用命令：
  help     - 显示此帮助信息
  mcp      - 使用MCP模式运行Agent
  normal   - 使用普通模式运行Agent
  quit     - 退出系统
  
使用示例：
  输入问题直接询问Agent(使用默认MCP模式)
  输入 "mcp 你的问题" 使用MCP模式
  输入 "normal 你的问题" 使用普通模式
        """
        print(help_text)
        
    def run(self):
        self.welcome()
        self.display_help()
        while True:
            try:
                user_input = input("\n你> ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("CUI-X-FreeAS 已退出")
                    break     
                if user_input.lower() == 'help':
                    self.display_help()
                    continue
                parts = user_input.split(' ', 1)
                if len(parts) == 1:
                    query = parts[0]
                    use_mcp = "yes"
                else:
                    command, query = parts
                    if command.lower() == 'mcp':
                        use_mcp = "yes"
                    elif command.lower() == 'normal':
                        use_mcp = "no"
                    else:
                        query = user_input
                        use_mcp = "yes"
                if not query.strip():
                    print("请输入有效的问题！")
                    continue
                print("CUI X-FreeAS> 已收到你的问题,正在处理……")
                result = Agent.AgentMain(query, self.current_dir, use_mcp)
            except KeyboardInterrupt:
                print("\n\n检测到中断,正在退出...")
                break
            except Exception as e:
                print(f"\n发生错误: {str(e)}")
                print("请输入 'help' 获取帮助")

def main():
    capp = CUIXFreeAS()
    capp.run()

if __name__ == "__main__":
    main()