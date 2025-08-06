# CUIX-HiOS 计划器系统

## 概述

CUIX-HiOS计划器系统是一个多智能体协作的项目管理工具，提供Todo.md生成、Workflow管理和实时任务跟踪功能。

## 特性

- **Todo.md生成器**：自动生成格式化的任务清单
- **工作流管理**：创建和管理多Agent协作流程
- **实时任务跟踪**：监控任务进度和状态
- **事件监控**：实时任务事件和警告通知
- **API接口**：简洁易用的接口供Agent调用
- **Mermaid支持**：自动生成流程图

## 文件结构

```
Framework/Planner/
├── planner_system.py    # 核心计划器系统
├── task_monitor.py      # 实时任务监控器
├── __init__.py         # 模块接口
├── example_usage.py    # 使用示例
├── Todo.md            # 生成的任务清单
├── workflows/          # 工作流文件目录
│   ├── 开发工作流_xxx.json
│   └── 质量保障工作流_xxx.json
├── task_tracker.json   # 任务跟踪数据
├── task_events.json    # 任务事件日志
├── monitor_status.json # 监控状态
└── todo_data.json      # Todo原始数据
```

## 使用方法

### 1. 基础使用

```python
from Framework.Planner import planner_system

# 创建项目计划
plan_result = planner_system.create_project_plan(
    "项目名称",
    tasks=[
        {
            "title": "任务1",
            "description": "任务描述",
            "priority": "high",  # high/medium/low
            "status": "pending",  # pending/in_progress/completed
            "deadline": "2025-08-10"
        }
    ],
    workflows=[
        {
            "name": "工作流名称",
            "description": "工作流描述",
            "steps": [
                {"name": "步骤1", "agent": "XNCoder", "condition": "条件"},
                {"name": "步骤2", "agent": "XSThinkingAgent", "condition": "条件"}
            ]
        }
    ],
    context="项目背景描述"
)
```

### 2. 简化API

```python
from Framework.Planner import (
    create_todo, add_task, create_workflow,
    start_task, update_task, complete_task,
    get_task_status, get_project_overview
)

# Todo管理
todo_path = create_todo("任务清单", tasks)
task_id = add_task("新任务", "任务描述", "high")

# 工作流管理
workflow_path = create_workflow("工作流名称", steps)

# 任务跟踪
start_task("task_001", "任务标题", estimated_hours=4)
update_task("task_001", 50, "进度更新")
complete_task("task_001", "完成说明")

# 状态查询
status = get_task_status("task_001")
overview = get_project_overview()
```

### 3. 工作流示例

```python
# 创建工作流
steps = [
    {"name": "需求分析", "agent": "XDeepResearch", "condition": "需求文档完成"},
    {"name": "系统设计", "agent": "XSThinkingAgent", "condition": "设计文档完成"},
    {"name": "代码开发", "agent": "XNCoder", "condition": "设计通过"},
    {"name": "测试验证", "agent": "XFileOperator", "condition": "开发完成"},
    {"name": "部署上线", "agent": "XGUIUseAgent", "condition": "测试通过"}
]

workflow_path = create_workflow("开发工作流", steps, "标准开发流程")

# 生成Mermaid图
mermaid = planner_system.workflow_generator.generate_mermaid_diagram("开发工作流")
```

### 4. 实时监控

```python
from Framework.Planner.task_monitor import TaskMonitor

# 创建监控器
monitor = TaskMonitor("Framework/Planner")

# 添加事件观察者
def on_task_event(event):
    print(f"任务事件: {event.task_id} - {event.event_type}")

monitor.add_observer(on_task_event)

# 开始监控
monitor.start_monitoring(interval_seconds=30)

# 获取监控状态
status = monitor.get_monitor_status()
recent_events = monitor.get_recent_events(limit=5)

# 停止监控
monitor.stop_monitoring()
```

## 数据结构

### 任务数据结构

```json
{
  "id": "任务唯一ID",
  "title": "任务标题",
  "description": "任务描述",
  "priority": "high/medium/low",
  "status": "pending/in_progress/completed",
  "deadline": "2025-08-10",
  "estimated_hours": 4,
  "assignee": "负责Agent",
  "created_at": "创建时间",
  "updated_at": "更新时间"
}
```

### 工作流数据结构

```json
{
  "id": "工作流唯一ID",
  "name": "工作流名称",
  "description": "工作流描述",
  "steps": [
    {
      "name": "步骤名称",
      "agent": "执行Agent",
      "condition": "执行条件"
    }
  ],
  "created_at": "创建时间",
  "updated_at": "更新时间",
  "status": "active/completed"
}
```

### 任务跟踪数据结构

```json
{
  "active_tasks": {
    "task_id": {
      "title": "任务标题",
      "start_time": "开始时间",
      "estimated_hours": 4,
      "status": "in_progress",
      "progress": 50,
      "notes": [
        {
          "time": "时间戳",
          "note": "进度说明"
        }
      ]
    }
  },
  "completed_tasks": {
    "task_id": {
      "title": "任务标题",
      "start_time": "开始时间",
      "end_time": "完成时间",
      "actual_hours": 3.5,
      "completion_note": "完成说明"
    }
  },
  "statistics": {
    "total_tasks": 10,
    "completed_tasks": 8,
    "average_completion_time": 4.2
  }
}
```

## 集成指南

### 在Agent中使用

```python
from Framework.Planner import create_todo, start_task, update_task

class MyAgent:
    def handle_project_request(self, request):
        # 创建项目计划
        tasks = self.parse_tasks(request)
        todo_path = create_todo("新功能开发", tasks)
        
        # 开始跟踪
        for task in tasks:
            start_task(task['id'], task['title'], task['estimated_hours'])
        
        # 执行任务
        # ... 实际执行逻辑 ...
        
        # 更新进度
        update_task(task_id, 100, "任务完成")
```

### 工作流集成

```python
# 在Agent中调用工作流
from Framework.Planner import create_workflow

# 定义Agent协作流程
workflow_steps = [
    {"name": "需求分析", "agent": "XDeepResearch", "condition": "需求明确"},
    {"name": "代码生成", "agent": "XNCoder", "condition": "设计完成"},
    {"name": "代码审查", "agent": "XSThinkingAgent", "condition": "代码生成"},
    {"name": "部署测试", "agent": "XGUIUseAgent", "condition": "审查通过"}
]

create_workflow("智能Agent协作", workflow_steps)
```

## 监控和警告

### 自动警告

系统会自动监控以下情况：
- **逾期警告**：任务超过截止日期
- **进度警告**：任务进度落后于预期
- **截止日期临近**：任务将在24小时内到期

### 事件类型

- `start`: 任务开始
- `progress`: 进度更新
- `complete`: 任务完成
- `deadline_warning`: 逾期警告
- `deadline_approaching`: 截止日期临近
- `progress_warning`: 进度落后警告

## 最佳实践

1. **任务粒度**：建议任务时长控制在2-8小时
2. **优先级管理**：使用high/medium/low清晰标识
3. **定期更新**：每完成重要里程碑时更新进度
4. **工作流设计**：确保每个步骤都有明确的Agent负责
5. **监控频率**：根据项目复杂度调整监控间隔

## 故障排除

### 常见问题

1. **文件权限错误**：确保有写入Planner目录的权限
2. **JSON格式错误**：手动检查JSON文件格式
3. **任务ID冲突**：使用UUID确保任务ID唯一性

### 调试方法

```python
# 查看任务状态
print(planner_system.task_tracker.get_overview())

# 查看最近事件
from Framework.Planner.task_monitor import TaskMonitor
monitor = TaskMonitor("Framework/Planner")
print(monitor.get_recent_events(limit=10))

# 检查工作流文件
import os
print(os.listdir("Framework/Planner/workflows"))
```