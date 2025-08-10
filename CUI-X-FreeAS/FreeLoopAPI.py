import sys
import os
import json
import argparse
import asyncio
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Any, Optional
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from FreeLoop.Free_Executor import FreeExecutor, FreeAgentRouter, FreePlanner, FreeMemory

def FreeLoopAPI(userq: str) -> Dict[str, Any]:
    user_query = userq
    executor = FreeExecutor()
    try:
        result = executor.execute_task_flow(user_query)
        print(result)
    except Exception as e:
        return {"status": "error", "message": f"[错误] 执行过程中出现错误: {e}"}

def run_single_agent(agent_name: str, userq: str) -> Dict[str, Any]:
    try:
        agent_router = FreeAgentRouter()
        result = agent_router.execute("run_agent", agent_name=agent_name, userq=userq)
        return {
            "status": "success",
            "agent": agent_name,
            "result": result,
            "message": f"Agent {agent_name} 执行完成"
        }
    except Exception as e:
        return {
            "status": "error",
            "agent": agent_name,
            "message": f"Agent {agent_name} 执行失败: {str(e)}"
        }

def Parallel_run(agent_tasks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    results = []
    
def execute_agent_task(task):
    agent_name = task["agent"]
    userq = task["query"]
    return run_agent(agent_name, userq)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(agent_tasks)) as executor:
            future_to_task = {
                executor.submit(execute_agent_task, task): task 
                for task in agent_tasks
            }
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        "status": "error",
                        "agent": task["agent"],
                        "message": f"并行执行异常: {str(e)}"
                    })
    except Exception as e:
        return [{"status": "error", "message": f"并行执行失败: {str(e)}"}]
    return results

def Get_agents() -> List[Dict[str, Any]]:
    try:
        agent_router = FreeAgentRouter()
        agents = agent_router.execute("get_agents")
        return agents
    except Exception as e:
        return [{"status": "error", "message": f"获取Agent列表失败: {str(e)}"}]

def main():
    parser = argparse.ArgumentParser(description='FreeLoopAPI - 智能体任务执行工具')
    parser.add_argument('--query', '-q', type=str, help='用户查询内容')
    parser.add_argument('--agent', '-a', type=str, help='指定单个Agent名称')
    parser.add_argument('--parallel', '-p', action='store_true', help='启用并行多Agent模式')
    parser.add_argument('--list-agents', '-l', action='store_true', help='列出所有可用Agent')
    args = parser.parse_args()
    try:
        if args.list_agents:
            agents = Get_agents()
            if agents and isinstance(agents, list) and len(agents) > 0:
                print("\n=== 可用Agent列表 ===")
                for agent in agents:
                    if isinstance(agent, dict) and 'name' in agent:
                        print(f"- {agent['name']}: {agent.get('description', '无描述')}")
                    else:
                        print(f"- {agent}")
            else:
                print("未找到可用Agent")
            return
        if not args.query:
            print("请输入内容，或查看帮助: python FreeLoopAPI.py --help")
        else:
            if args.parallel:
                agents = Get_agents()
                if not agents or len(agents) == 0:
                    print("未找到可用Agent")
                    return
                print(f"\n=== 并行执行模式 ===")
                print(f"内容: {args.query}")
                print(f"Agent数量: {len(agents)}")
                agent_tasks = []
                for agent in agents:
                    if isinstance(agent, dict) and 'name' in agent:
                        agent_tasks.append({
                            "agent": agent['name'],
                            "query": args.query
                        })
                if agent_tasks:
                    results = Parallel_run(agent_tasks)
                    print_results(results)
                else:
                    print("没有可用的Agent任务")
            elif args.agent:
                print(f"\n=== 单Agent模式 ===")
                print(f"Agent: {args.agent}")
                print(f"内容: {args.query}")
                result = run_single_agent(args.agent, args.query)
                print_result(result)
            else:
                print(f"\n=== 正常模式 ===")
                print(f"内容: {args.query}")
                result = FreeLoopAPI(args.query)
                print_result(result)
    except KeyboardInterrupt:
        print("\n用户中断, 程序退出")
    except Exception as e:
        print(f"执行错误: {e}")

def print_result(result):
    if isinstance(result, dict):
        if result.get("status") == "success":
            if "result" in result:
                return {"status": "success", "message": result["result"]}
            elif "message" in result:
                return {"status": "success", "message": result["message"]}
            elif "execution_results" in result:
                execution_results = result["execution_results"]
                if isinstance(execution_results, list):
                    formatted_results = []
                    for res in execution_results:
                        if isinstance(res, dict):
                            task_name = res.get("task", "未知任务")
                            agent_name = res.get("agent", "未知Agent")
                            task_result = res.get("result", "无结果")
                            formatted_results.append(f"任务: {task_name}, Agent: {agent_name}, 结果: {task_result}")
                        else:
                            formatted_results.append(str(res))
                    return {"status": "success", "message": "\n".join(formatted_results)}
                else:
                    return {"status": "success", "message": str(execution_results)}
            else:
                return {"status": "success", "message": str(result)}
        else:
            return {"status": "error", "message": result.get("message", "未知错误")}
    else:
        if result is not None:
            return {"status": "success", "message": str(result)}
        else:
            return {"status": "success", "message": "任务执行完成"}

def print_results(results):
    if isinstance(results, list):
        print(f"\n执行结果汇总 (共{len(results)}个Agent):")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.get('agent', '未知Agent')}:")
            print_result(result)
    else:
        print_result(results)

if __name__ == "__main__":
    main()
