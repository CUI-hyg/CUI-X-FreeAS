import os
import sys
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from Framework.AgentRouter.AgentRouter import AgentRouter as FrameworkAgentRouter
from Framework.Planner.Planner import TodoControl, WorkFlowCreator
from Framework.Memory.Memory import MemorySystem

class FreeMemory:
    def __init__(self):
        self.memory_system = MemorySystem()
    
    def execute(self, action: str, **kwargs) -> Any: 
        if action == "add":
            content = kwargs.get("content")
            memory_type = kwargs.get("memory_type", "short_term")
            keywords = kwargs.get("keywords", [])
            importance = kwargs.get("importance", 5)
            if memory_type == "short_term":
                return self.memory_system.st_mem_add(content, keywords)
            elif memory_type == "long_term":
                return self.memory_system.lt_mem_add(content, keywords, importance)
            else:
                raise ValueError("memory_type must be 'short_term' or 'long_term'")
        elif action == "search":
            query = kwargs.get("query")
            memory_type = kwargs.get("memory_type", "all")
            return self.memory_system.search_mem(query, memory_type)
        elif action == "get":
            memory_type = kwargs.get("memory_type", "all")
            return self.memory_system.get_all_mem(memory_type)
        elif action == "delete":
            memory_id = kwargs.get("memory_id")
            if memory_id:
                return self.memory_system.del_mem(memory_id)
            else:
                raise ValueError("memory_id is required for delete action")
        elif action == "clean":
            memory_type = kwargs.get("memory_type", "short_term")
            if memory_type == "short_term":
                self.memory_system.clean_sm()
                return "Short term memory cleaned"
            else:
                raise ValueError("Only short_term memory can be cleaned")
        else:
            raise ValueError(f"Unsupported action: {action}")

class FreePlanner:
    def __init__(self):
        from Framework.Planner.Planner import TodoControl, WorkFlowCreator
        self.todo_control = None
        self.workflow_creator = None
        self.current_userq = None
    
    def execute(self, action: str, **kwargs) -> Any:
        if action == "create_todo":
            userq = kwargs.get("userq")
            if not userq:
                raise ValueError("userq is required for create_todo")
            self.current_userq = userq
            self.todo_control = TodoControl(userq)
            self.todo_control.create_todo()
            return "todo.md已生成"
        elif action == "read_todo":
            if not self.todo_control:
                raise ValueError("No todo control initialized. Call create_todo first.")
            return self.todo_control.read_todo()
        elif action == "tick_task":
            task = kwargs.get("task")
            if not task:
                raise ValueError("task is required for tick_task")
            if not self.todo_control:
                raise ValueError("No todo control initialized. Call create_todo first.")
            return self.todo_control.tick_task(task)
        elif action == "create_workflow":
            userq = kwargs.get("userq")
            if not userq:
                raise ValueError("userq is required for create_workflow")
            self.current_userq = userq
            self.workflow_creator = WorkFlowCreator(userq)
            result = self.workflow_creator.todo2workflow()
            return result
        elif action == "extract_workflow":
            if not self.workflow_creator:
                raise ValueError("No workflow creator initialized. Call create_workflow first.")
            return self.workflow_creator.extract_workflow()
        elif action == "todo2workflow":
            if not self.workflow_creator:
                raise ValueError("No workflow creator initialized. Call create_workflow first.")
            if not self.todo_control:
                raise ValueError("No todo control initialized. Call create_todo first.")
            todo_content = self.todo_control.read_todo()
            return self.workflow_creator.todo2workflow(todo_content)
        else:
            raise ValueError(f"Unsupported action: {action}")

class FreeAgentRouter:
    def __init__(self):
        self.current_agent = None
        self.current_userq = None
        self.current_tool = None
    
    def execute(self, action: str, **kwargs) -> Any:
        if action == "get_agents":
            router = FrameworkAgentRouter("", "", "")
            return router.get_all_agents()
        elif action == "run_agent":
            agent_name = kwargs.get("agent_name")
            userq = kwargs.get("userq")
            agent_use_tool = kwargs.get("agent_use_tool", "no")
            if not agent_name:
                raise ValueError("agent_name is required for run_agent")
            if not userq:
                raise ValueError("userq is required for run_agent")
            self.current_agent = agent_name
            self.current_userq = userq
            self.current_tool = agent_use_tool
            router = FrameworkAgentRouter(agent_name, userq, agent_use_tool)
            return router.main_loop()
        elif action == "get_agent_info":
            agent_name = kwargs.get("agent_name")
            if not agent_name:
                raise ValueError("agent_name is required for get_agent_info")
            router = FrameworkAgentRouter(agent_name, "", "")
            agents = router.get_all_agents()
            for agent in agents:
                if agent["name"] == agent_name:
                    return agent
            return None
        else:
            raise ValueError(f"Unsupported action: {action}")

class FreeExecutor:
    def __init__(self):
        self.agent_router = FreeAgentRouter()
        self.memory = FreeMemory()
        self.planner = FreePlanner()
    
    def execute_task_flow(self, user_query: str) -> Dict[str, Any]:
        """
        执行完整的任务流程：
        1. 创建todo.md
        2. todo.md转workflow
        3. 解析workflow
        4. 调用agent_router执行任务
        5. 阅读todo.md
        6. 将已完成任务打勾
        7. 存入长期记忆
        8. 向用户反馈结果
        """
        try:
            self.planner.execute("create_todo", userq=user_query)
            self.planner.execute("create_workflow", userq=user_query)
            workflow_data = self.planner.execute("extract_workflow")
            if not workflow_data:
                return {"status": "error", "message": "无法解析workflow"}
            if isinstance(workflow_data, str):
                try:
                    workflow_data = json.loads(workflow_data)
                except json.JSONDecodeError:
                    return {"status": "error", "message": "workflow数据格式错误"}
            execution_results = []
            for task in workflow_data.get("tasks", []):
                task_name = task.get("name")
                task_description = task.get("description")
                agent_name = task.get("agent")
                agent_query = f"任务: {task_name}\n描述: {task_description}"
                agent_result = self.agent_router.execute("run_agent", agent_name=agent_name, userq=agent_query)
                execution_results.append({
                    "task": task_name,
                    "agent": agent_name,
                    "result": agent_result,
                    "status": "completed"
                })
                self.planner.execute("tick_task", task=task_name)
            memory_content = {
                "user_query": user_query,
                "workflow": workflow_data,
                "execution_results": execution_results,
                "completed_at": datetime.now().isoformat()
            }
            self.memory.execute("add", content=json.dumps(memory_content, ensure_ascii=False),memory_type="long_term",keywords=["task_execution", user_query, "workflow"],importance=8)
            try:
                updated_todo = self.planner.execute("read_todo")
            except Exception:
                updated_todo = "无法读取更新后的todo.md"
            try:
                context_content = f"""任务执行完成报告
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
用户查询: {user_query}

工作流详情:
{json.dumps(workflow_data, ensure_ascii=False, indent=2)}

执行结果:
{json.dumps(execution_results, ensure_ascii=False, indent=2)}

已完成的任务数: {len(execution_results)}
"""
                context_file_path = os.path.join(project_root, 'context.txt')
                print(f"准备写入上下文文件: {context_file_path}")
                print(f"内容长度: {len(context_content)} 字符")
                with open(context_file_path, 'w', encoding='utf-8') as f:
                    f.write(context_content)
                print(f"上下文已成功保存到: {context_file_path}")
                print(f"文件大小: {os.path.getsize(context_file_path)} 字节")
            except Exception as save_error:
                print(f"警告: 保存上下文文件失败 - {save_error}")
                import traceback
                traceback.print_exc()
            return {
                "status": "success",
                "message": "任务流程执行完成",
                "user_query": user_query,
                "workflow": workflow_data,
                "execution_results": execution_results,
                "updated_todo": updated_todo,
                "memory_stored": True,
                "context_saved": True
            }
        except Exception as e:
            error_info = {
                "status": "error",
                "message": str(e),
                "user_query": user_query,
                "error_type": type(e).__name__,
                "timestamp": datetime.now().isoformat()
            }
            return error_info
    
    def run_single_task(self, task_name: str, task_description: str, agent_name: str = "XSThinkingAgent") -> Dict[str, Any]:
        try:
            agent_query = f"任务: {task_name}\n描述: {task_description}"
            result = self.agent_router.execute("run_agent", agent_name=agent_name,userq=agent_query)
            memory_content = {
                "task_name": task_name,
                "task_description": task_description,
                "agent_name": agent_name,
                "result": result,
                "completed_at": datetime.now().isoformat()
            }
            self.memory.execute("add",
                              content=json.dumps(memory_content, ensure_ascii=False),
                              memory_type="long_term",
                              keywords=["single_task", task_name, agent_name],
                              importance=7)
            # 保存单个任务结果到上下文文件
            try:
                context_content = f"""单任务执行完成报告
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
任务名称: {task_name}
任务描述: {task_description}
使用Agent: {agent_name}

执行结果:
{json.dumps(result, ensure_ascii=False, indent=2)}
"""
                context_file_path = os.path.join(project_root, 'context.txt')
                with open(context_file_path, 'w', encoding='utf-8') as f:
                    f.write(context_content)
                print(f"上下文已保存到: {context_file_path}")
            except Exception as save_error:
                print(f"警告: 保存上下文文件失败 - {save_error}")
                
            return {
                "status": "success",
                "task_name": task_name,
                "result": result,
                "context_saved": True
            }
        except Exception as e:
            return {
                "status": "error",
                "task_name": task_name,
                "error": str(e)
            }