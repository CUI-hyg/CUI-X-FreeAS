import sys
import os
import json
from datetime import datetime
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from Free_Executor import FreeExecutor, FreeAgentRouter, FreePlanner, FreeMemory

def demo_execute_task_flow():
    """演示完整的任务执行流程"""
    print("=" * 60)
    print("FreeLoop 完整任务流程演示")
    print("=" * 60)
    
    # 创建执行器实例
    executor = FreeExecutor()
    
    # 示例用户查询
    user_query = "请帮我创建一个Python数据分析项目，包括数据清洗、可视化和报告生成"
    
    print(f"用户查询: {user_query}")
    print("-" * 50)
    
    try:
        # 执行完整任务流程
        result = executor.execute_task_flow(user_query)
        
        # 显示结果摘要
        if result["status"] == "success":
            print("[成功] 任务执行成功!")
            print(f"工作流任务数: {len(result['workflow'].get('tasks', []))}")
            print(f"执行结果数: {len(result['execution_results'])}")
            print(f"已存入长期记忆")
            
            # 显示工作流任务
            if result["workflow"].get("tasks"):
                print("\n工作流任务:")
                for task in result["workflow"]["tasks"]:
                    print(f"  - {task.get('name', '未知任务')}: {task.get('description', '无描述')}")
            
            # 显示执行结果
            if result["execution_results"]:
                print("\n执行结果:")
                for res in result["execution_results"]:
                    print(f"  - {res['task']}: {res['status']}")
                    if 'result' in res:
                        print(f"    结果预览: {str(res['result'])[:100]}...")
            
            # 显示更新后的todo
            if result.get("updated_todo"):
                print(f"\ntodo.md已更新")
                
        else:
            print(f"[错误] 任务执行失败: {result['message']}")
            
    except Exception as e:
        print(f"[错误] 执行过程中出现错误: {e}")
    
    print("\n" + "=" * 60)

def demo_single_task():
    """演示单个任务执行"""
    print("\n" + "=" * 60)
    print("单个任务执行演示")
    print("=" * 60)
    
    executor = FreeExecutor()
    
    # 单个任务示例
    task_name = "代码质量分析"
    task_description = "分析当前项目的代码质量，包括代码规范、复杂度、测试覆盖率"
    
    print(f"任务: {task_name}")
    print(f"描述: {task_description}")
    
    result = executor.run_single_task(task_name, task_description, "XSThinkingAgent")
    
    if result["status"] == "success":
        print("✅ 任务执行成功!")
        print(f"结果: {str(result['result'])[:200]}...")
    else:
        print(f"❌ 任务执行失败: {result['error']}")

def demo_memory_integration():
    """演示记忆集成功能"""
    print("\n" + "=" * 60)
    print("记忆集成演示")
    print("=" * 60)
    
    executor = FreeExecutor()
    
    try:
        memories = executor.memory.execute("get", memory_type="long_term")
        print(f"长期记忆总数: {len(memories)}")
        if memories:
            print("\n最近的记忆:")
            for i, memory in enumerate(memories[-3:], 1):
                content = memory.get('content', '{}')
                try:
                    if not content or not content.strip():
                        print(f"{i}. [空内容]")
                        continue
                    data = json.loads(content)
                    if isinstance(data, dict) and 'task_name' in data:
                        print(f"{i}. 任务: {data['task_name']}")
                    elif isinstance(data, dict) and 'user_query' in data:
                        print(f"{i}. 查询: {data['user_query']}")
                    else:
                        print(f"{i}. {content[:100]}...")
                except json.JSONDecodeError:
                    print(f"{i}. [无效JSON] {content[:100]}...")
                except Exception as e:
                    print(f"{i}. [错误] {str(e)[:50]}...")
        search_result = executor.memory.execute("search", 
                                           query="task_execution", 
                                           memory_type="long_term")
        print(f"\n任务执行相关记忆数: {len(search_result)}")
        
    except Exception as e:
        print(f"记忆演示错误: {e}")

def demo_agent_exploration():
    """演示Agent探索功能"""
    print("\n" + "=" * 60)
    print("Agent探索演示")
    print("=" * 60)
    executor = FreeAgentRouter()
    try:
        # 获取所有可用Agent
        agents = executor.execute("get_agents")
        print(f"可用Agent总数: {len(agents)}")
        # 显示Agent信息
        print("\nAgent列表:")
        for agent in agents:
            print(f"- {agent['name']}")
            if 'description' in agent:
                print(f"  描述: {agent['description']}")
            if 'capabilities' in agent:
                print(f"  能力: {', '.join(agent['capabilities'])}")
    except Exception as e:
        print(f"Agent探索错误: {e}")

def main():
    """主函数"""
    print("FreeLoop 新执行流程演示")
    print("当前时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        # 演示Agent探索（先了解可用Agent）
        demo_agent_exploration()
        
        # 演示完整任务流程
        demo_execute_task_flow()
        
        # 演示单个任务
        demo_single_task()
        
        # 演示记忆集成
        demo_memory_integration()
        
        print("\n" + "=" * 60)
        print("所有演示完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()