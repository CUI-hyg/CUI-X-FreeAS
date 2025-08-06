import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Framework.Planner import planner_system, task_monitor
from Framework.Planner.task_monitor import TaskMonitor

def demo_planner_system():
    """演示计划器系统的完整功能"""
    print("=== CUIX-HiOS 计划器系统演示 ===\n")
    # 1. 创建项目计划
    print("1. 创建项目计划...")
    # 定义任务
    tasks = [
        {
            "title": "需求分析",
            "description": "收集和分析用户需求",
            "priority": "high",
            "status": "pending",
            "estimated_hours": 4
        },
        {
            "title": "系统设计",
            "description": "设计系统架构和数据库",
            "priority": "high", 
            "status": "pending",
            "estimated_hours": 6
        },
        {
            "title": "代码开发",
            "description": "实现核心功能",
            "priority": "medium",
            "status": "pending",
            "estimated_hours": 16
        },
        {
            "title": "测试验证",
            "description": "进行单元测试和集成测试",
            "priority": "medium",
            "status": "pending", 
            "estimated_hours": 8
        },
        {
            "title": "部署上线",
            "description": "部署到生产环境",
            "priority": "low",
            "status": "pending",
            "estimated_hours": 4
        }
    ]
    # 定义工作流
    workflows = [
        {
            "name": "开发工作流",
            "description": "标准开发流程",
            "steps": [
                {"name": "需求分析", "agent": "XDeepResearch", "condition": "需求文档完成"},
                {"name": "系统设计", "agent": "XSThinkingAgent", "condition": "设计文档完成"},
                {"name": "代码开发", "agent": "XNCoder", "condition": "设计通过"},
                {"name": "测试验证", "agent": "XFileOperator", "condition": "开发完成"},
                {"name": "部署上线", "agent": "XGUIUseAgent", "condition": "测试通过"}
            ]
        }
    ]
    # 创建完整项目计划
    plan_result = planner_system.create_project_plan(
        "CUIX-HiOS功能开发",
        tasks,
        workflows,
        "开发CUIX-HiOS的记忆系统和计划器功能"
    )
    print(f"Todo文件: {plan_result['todo_file']}")
    print(f"工作流文件: {plan_result['workflow_files']}")
    # 2. 添加额外任务
    print("\n2. 添加额外任务...")
    task_id = planner_system.todo_generator.add_task(
        "文档编写",
        "编写用户使用手册",
        priority="medium",
        deadline="2025-08-10"
    )
    print(f"添加任务ID: {task_id}")
    # 3. 创建额外工作流
    print("\n3. 创建工作流...")
    workflow_steps = [
        {"name": "代码审查", "agent": "XNCoder", "condition": "开发完成"},
        {"name": "性能优化", "agent": "XSThinkingAgent", "condition": "审查通过"},
        {"name": "用户测试", "agent": "XGUIUseAgent", "condition": "优化完成"}
    ]
    workflow_path = planner_system.workflow_generator.create_workflow(
        "质量保障工作流",
        workflow_steps,
        "确保代码质量的完整流程"
    )
    print(f"工作流文件: {workflow_path}")
    # 4. 生成Mermaid图
    print("\n4. 生成Mermaid流程图...")
    mermaid = planner_system.workflow_generator.generate_mermaid_diagram("开发工作流")
    print("Mermaid图已生成")
    # 5. 任务跟踪演示
    print("\n5. 任务跟踪演示...")
    # 开始跟踪任务
    sample_task_id = "task_001"
    planner_system.task_tracker.start_task(sample_task_id, "需求分析", 4)
    # 更新进度
    planner_system.task_tracker.update_progress(sample_task_id, 25, "开始收集用户反馈")
    time.sleep(1)  # 模拟工作
    planner_system.task_tracker.update_progress(sample_task_id, 50, "完成初步需求整理")
    time.sleep(1)
    planner_system.task_tracker.update_progress(sample_task_id, 100, "需求文档完成")
    # 完成任务
    planner_system.task_tracker.complete_task(sample_task_id, "需求分析已完成，文档已提交")
    # 6. 实时监控演示
    print("\n6. 实时监控演示...")
    # 创建监控器
    monitor = TaskMonitor(planner_system.planner_dir)
    # 添加事件观察者
    def on_task_event(event):
        print(f"📊 任务事件: {event.task_id} - {event.event_type}")
    monitor.add_observer(on_task_event)
    # 开始监控
    monitor.start_monitoring(interval_seconds=5)
    # 模拟一些任务活动
    task_id2 = "task_002"
    planner_system.task_tracker.start_task(task_id2, "系统设计", 6)
    time.sleep(2)
    planner_system.task_tracker.update_progress(task_id2, 30)
    time.sleep(2)
    planner_system.task_tracker.complete_task(task_id2, "设计完成")
    monitor.stop_monitoring()
    # 7. 获取项目概览
    print("\n7. 项目概览...")
    overview = planner_system.task_tracker.get_overview()
    print(f"活跃任务: {overview['active_tasks_count']}")
    print(f"已完成任务: {overview['completed_tasks_count']}")
    print(f"平均完成时间: {overview['statistics']['average_completion_time']:.1f}小时")
    # 8. 获取任务状态
    print("\n8. 任务状态查询...")
    status = planner_system.task_tracker.get_task_status(sample_task_id)
    if status:
        print(f"任务 {sample_task_id} 状态:")
        print(f"  标题: {status['title']}")
        print(f"  状态: {status['status']}")
        print(f"  开始时间: {status['start_time']}")
        if 'end_time' in status:
            print(f"  完成时间: {status['end_time']}")
            print(f"  实际用时: {status['actual_hours']:.1f}小时")

def demo_simple_api():
    """演示简化API的使用"""
    print("\n=== 简化API演示 ===\n")
    from Framework.Planner import (
        create_todo, add_task, create_workflow,
        start_task, update_task, complete_task, get_task_status
    )
    # 使用简化API创建todo
    simple_tasks = [
        {"title": "API测试", "description": "测试简化API", "priority": "high", "status": "pending"}
    ]
    todo_path = create_todo("简化API测试", simple_tasks)
    print(f"简化API创建Todo: {todo_path}")
    # 添加任务
    new_task_id = add_task("简化任务", "通过简化API添加", "medium")
    print(f"简化API添加任务: {new_task_id}")
    # 任务跟踪
    test_task_id = "simple_test"
    start_task(test_task_id, "简化API测试", 2)
    update_task(test_task_id, 50, "进行中")
    complete_task(test_task_id, "简化API测试完成")    
    status = get_task_status(test_task_id)
    print(f"简化API任务状态: {status['status']}")

if __name__ == "__main__":
    demo_planner_system()
    demo_simple_api()
    print("\n=== 演示完成 ===")
    print("检查生成的文件:")
    print("- Framework/Planner/Todo.md")
    print("- Framework/Planner/data/ 目录")
    print("- Framework/Planner/workflows/ 目录")