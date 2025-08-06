import sys
import os
import json
from datetime import datetime

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from FreeLoop import (
    executor, execute_task, get_agents, 
    get_task_history, get_task_status, get_project_overview
)

def demo_basic_usage():
    """基础使用演示"""
    print("=" * 50)
    print("FreeLoop系统基础使用演示")
    print("=" * 50)
    
    # 1. 查看可用Agent
    print("\n1. 可用Agent列表:")
    agents = get_agents()
    for agent in agents:
        print(f"  - {agent['name']}: {agent['description']}")
        print(f"    能力: {', '.join(agent['capabilities'])}")
    
    # 2. 执行简单任务
    print("\n2. 执行任务:")
    task1 = "搜索Python最佳实践文档"
    result1 = execute_task(task1, agent_type="auto")
    print(f"任务: {task1}")
    print(f"结果: {json.dumps(result1, ensure_ascii=False, indent=2)}")
    
    # 3. 执行另一个任务
    task2 = "分析当前代码质量"
    context = {"project_path": project_root, "language": "python"}
    result2 = execute_task(task2, agent_type="auto", context=context)
    print(f"\n任务: {task2}")
    print(f"结果: {json.dumps(result2, ensure_ascii=False, indent=2)}")

def demo_advanced_usage():
    """高级功能演示"""
    print("\n" + "=" * 50)
    print("高级功能演示")
    print("=" * 50)
    
    # 1. 批量任务执行
    print("\n1. 批量任务执行:")
    tasks = [
        "优化数据库查询性能",
        "重构用户认证模块",
        "添加单元测试覆盖率"
    ]
    
    task_results = []
    for task in tasks:
        result = execute_task(task, agent_type="auto")
        task_results.append({
            "task": task,
            "status": "success" if "error" not in result else "failed",
            "task_id": result.get("task_id")
        })
    
    print("批量任务执行完成:")
    for result in task_results:
        print(f"  - {result['task']}: {result['status']}")
    
    # 2. 查看任务历史
    print("\n2. 任务历史:")
    history = get_task_history(5)
    for i, memory in enumerate(history, 1):
        print(f"  {i}. {memory['content'][:100]}...")
    
    # 3. 项目概览
    print("\n3. 项目概览:")
    overview = get_project_overview()
    print(json.dumps(overview, ensure_ascii=False, indent=2))

def demo_error_handling():
    """错误处理演示"""
    print("\n" + "=" * 50)
    print("错误处理演示")
    print("=" * 50)
    
    # 执行不存在的Agent类型
    print("\n1. 测试错误Agent类型:")
    result = execute_task("测试任务", agent_type="non_existent_agent")
    print(f"错误结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 空任务描述
    print("\n2. 测试空任务描述:")
    result = execute_task("")
    print(f"空任务结果: {json.dumps(result, ensure_ascii=False, indent=2)}")

def demo_task_tracking():
    """任务跟踪演示"""
    print("\n" + "=" * 50)
    print("任务跟踪演示")
    print("=" * 50)
    
    # 创建一个复杂任务并跟踪
    complex_task = "开发完整的Web应用API"
    context = {
        "requirements": [
            "用户认证系统",
            "RESTful API设计",
            "数据库集成",
            "单元测试"
        ],
        "tech_stack": ["FastAPI", "PostgreSQL", "SQLAlchemy"],
        "timeline": "2周"
    }
    
    print(f"\n执行复杂任务: {complex_task}")
    result = execute_task(complex_task, agent_type="auto", context=context)
    
    if result.get("task_id"):
        task_id = result["task_id"]
        
        # 查看任务状态
        print(f"\n任务ID: {task_id}")
        status = get_task_status(task_id)
        if status:
            print("任务状态:")
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print("任务状态: 未找到")

def main():
    """主函数 - 运行所有演示"""
    print("FreeLoop系统完整演示")
    print("当前时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    try:
        # 基础使用
        demo_basic_usage()
        
        # 高级功能
        demo_advanced_usage()
        
        # 任务跟踪
        demo_task_tracking()
        
        # 错误处理
        demo_error_handling()
        
        print("\n" + "=" * 50)
        print("演示完成！")
        print("=" * 50)
        
        # 最终项目概览
        print("\n最终项目概览:")
        final_overview = get_project_overview()
        print(json.dumps(final_overview, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()