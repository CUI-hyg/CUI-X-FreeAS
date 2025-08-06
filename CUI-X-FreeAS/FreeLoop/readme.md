# FreeLoop - 总调用功能系统

FreeLoop是一个完整的Agent执行器系统，整合了Agent管理、任务规划、记忆存储和实时跟踪功能。

## 系统概述

FreeLoop系统包含三个核心组件：
- **AgentExecutor**: 总调度器，负责任务执行的全流程管理
- **AgentManager**: Agent管理器，自动发现和动态加载Agent
- **TaskCoordinator**: 任务协调器，负责任务规划和执行跟踪

## 功能特性

### 🎯 核心功能
- **自动Agent发现**: 自动扫描并加载Agents目录下的所有Agent
- **智能Agent选择**: 根据任务描述自动选择最适合的Agent
- **任务规划**: 集成Planner系统，自动生成任务清单和工作流
- **记忆管理**: 集成Memory系统，存储任务历史和执行结果
- **实时跟踪**: 监控任务执行进度和状态
- **错误处理**: 完善的错误捕获和日志记录

### 🔧 Agent管理
- 动态模块导入
- Agent能力分析
- 自动Agent选择算法
- 支持多种Agent接口

### 📊 任务管理
- Todo.md自动生成
- 工作流配置生成
- Mermaid流程图支持
- 任务进度实时更新

### 🧠 记忆系统
- 短期记忆存储
- 长期记忆存储
- 智能搜索和索引
- 任务历史追踪

## 文件结构

```
FreeLoop/
├── AgentExecutor.py      # 核心执行器实现
├── __init__.py          # 接口文件
├── example_usage.py     # 使用示例
├── README.md           # 本文档
└── data/               # 运行时数据文件
    ├── todo_data.json
    ├── task_tracker.json
    └── workflows/
```

## 安装和使用

### 基本使用

```python
from FreeLoop import execute_task, get_agents

# 执行单个任务
result = execute_task("搜索Python最佳实践")
print(result)

# 查看可用Agent
agents = get_agents()
for agent in agents:
    print(f"Agent: {agent['name']}, 能力: {agent['capabilities']}")
```

### 高级使用

```python
from FreeLoop import AgentExecutor

# 创建执行器实例
executor = AgentExecutor()

# 指定Agent类型
result = executor.execute_task(
    "分析代码质量", 
    agent_type="XTestAgent",
    context={"project_path": "/path/to/project"}
)
```

## API参考

### 简化API函数

#### `execute_task(task_description, agent_type="auto", context=None)`
执行任务的简化接口。

**参数:**
- `task_description` (str): 任务描述
- `agent_type` (str): Agent类型，默认为"auto"自动选择
- `context` (dict): 任务上下文信息

**返回:**
- 任务执行结果字典

#### `get_agents()`
获取所有可用Agent列表。

**返回:**
- Agent信息列表

#### `get_task_history(limit=10)`
获取任务历史记录。

**参数:**
- `limit` (int): 返回的记录数量限制

**返回:**
- 任务历史记录列表

#### `get_task_status(task_id)`
获取指定任务的状态。

**参数:**
- `task_id` (str): 任务ID

**返回:**
- 任务状态信息字典

#### `get_project_overview()`
获取项目概览信息。

**返回:**
- 项目统计和状态信息字典

### 新执行流程API

#### `FreeExecutor`
全新的执行器类，实现了完整的任务流程。

**方法:**
- `execute_task_flow(user_query: str) -> Dict[str, Any]`: 执行完整任务流程
  - 自动创建todo.md任务清单
  - 将todo.md转换为workflow工作流
  - 解析workflow获取任务列表
  - 调用agent_router执行每个任务
  - 标记已完成任务
  - 将结果存入长期记忆
  - 返回完整执行结果

- `run_single_task(task_name: str, task_description: str, agent_name: str = "XSThinkingAgent") -> Dict[str, Any]`: 运行单个任务
  - 直接调用指定Agent执行任务
  - 将结果存入长期记忆
  - 返回任务执行结果

#### 完整流程步骤
使用`execute_task_flow`方法时，系统会自动执行以下8个步骤：

1. **创建todo.md**: 根据用户查询自动生成任务清单
2. **todo.md转workflow**: 将任务清单转换为可执行的工作流
3. **解析workflow**: 提取具体任务和Agent分配信息
4. **调用agent_router**: 为每个任务调用相应的Agent执行
5. **阅读todo.md**: 获取当前任务状态
6. **标记完成任务**: 将已完成的任务打勾
7. **存入长期记忆**: 将整个执行过程存入记忆系统
8. **向用户反馈**: 返回完整的执行结果和状态

#### 返回结果结构
`execute_task_flow`返回的字典包含：
```python
{
    "status": "success" | "error",
    "message": "执行状态描述",
    "user_query": "原始用户查询",
    "workflow": {
        "tasks": [
            {
                "name": "任务名称",
                "description": "任务描述",
                "agent": "指定Agent"
            }
        ]
    },
    "execution_results": [
        {
            "task": "任务名称",
            "agent": "执行Agent",
            "result": "执行结果",
            "status": "completed"
        }
    ],
    "updated_todo": "更新后的todo内容",
    "memory_stored": True
}
```

#### `AgentManager`
Agent管理器。

**方法:**
- `get_agent(agent_name)`: 获取指定Agent实例
- `select_best_agent(task_description)`: 根据任务选择最佳Agent
- `list_agents()`: 列出所有Agent

#### `TaskCoordinator`
任务协调器。

**方法:**
- `create_task_plan(task_description, agent, context)`: 创建任务计划
- `execute_plan(plan)`: 执行计划
- `get_task_status(task_id)`: 获取任务状态
- `get_project_overview()`: 获取项目概览

## 创建自定义Agent

### 步骤1: 创建Agent目录
在`Agents/`目录下创建新的Agent文件夹：

```
Agents/
└── YourAgent/
    ├── __init__.py
    └── YourAgent.py
```

### 步骤2: 实现Agent类

```python
class YourAgent:
    """你的Agent描述"""
    
    def __init__(self):
        self.name = "YourAgent"
        self.description = "Agent功能描述"
        self.supported_types = ["type1", "type2"]
    
    def execute(self, task_description: str, context: dict = None) -> dict:
        """执行任务的入口方法"""
        # 实现你的Agent逻辑
        return {
            "status": "success",
            "result": "任务执行结果",
            "details": "详细信息"
        }
```

### 步骤3: 自动发现
FreeLoop会自动发现并加载新的Agent，无需额外配置。

## 使用示例

### 示例1: 完整任务流程执行（新功能）
```python
from Free_Executor import FreeExecutor

# 创建执行器
executor = FreeExecutor()

# 执行完整任务流程：创建todo -> 转workflow -> 解析 -> 调用agent -> 标记完成 -> 存入记忆 -> 反馈结果
result = executor.execute_task_flow("请帮我创建一个Python数据分析项目，包括数据清洗、可视化和报告生成")

print(f"状态: {result['status']}")
print(f"工作流: {result['workflow']}")
print(f"执行结果: {result['execution_results']}")
print(f"已存入记忆: {result['memory_stored']}")
```

### 示例2: 单个任务执行
```python
from Free_Executor import FreeExecutor

executor = FreeExecutor()

# 运行单个任务
result = executor.run_single_task(
    task_name="代码质量分析",
    task_description="分析当前项目的代码质量，包括代码规范、复杂度、测试覆盖率",
    agent_name="XSThinkingAgent"
)

print(f"任务状态: {result['status']}")
print(f"执行结果: {result.get('result', '无结果')}")
```

### 示例3: 基本任务执行（兼容旧接口）
```python
from FreeLoop import execute_task

# 执行搜索任务
result = execute_task("搜索最新的机器学习框架")
print(f"搜索结果: {result['result']}")

# 执行分析任务
result = execute_task("分析当前项目架构")
print(f"分析结果: {result['result']}")
```

### 示例2: 批量任务处理
```python
from FreeLoop import execute_task

tasks = [
    "优化数据库查询",
    "添加缓存机制",
    "改进错误处理"
]

for task in tasks:
    result = execute_task(task)
    print(f"任务: {task} - 状态: {'成功' if 'error' not in result else '失败'}")
```

### 示例3: 状态监控
```python
from FreeLoop import get_task_status, get_project_overview

# 获取项目概览
overview = get_project_overview()
print(f"总任务数: {overview['statistics']['total_tasks']}")
print(f"已完成: {overview['statistics']['completed_tasks']}")

# 获取特定任务状态
task_id = "your_task_id"
status = get_task_status(task_id)
print(f"任务进度: {status.get('progress', 0)}%")
```

## 集成指南

### 与其他系统集成

#### 与Memory系统集成
FreeLoop自动使用Memory系统存储任务历史和执行结果。

#### 与Planner系统集成
FreeLoop自动创建任务计划、工作流和跟踪。

### 配置选项

#### 环境变量
```bash
# 设置Agent目录
export FREELOOP_AGENTS_DIR="/custom/agents/path"

# 设置数据目录
export FREELOOP_DATA_DIR="/custom/data/path"
```

#### 代码配置
```python
from FreeLoop import AgentExecutor

# 自定义配置
executor = AgentExecutor(
    agents_dir="/custom/agents",
    planner_dir="/custom/planner",
    memory_dir="/custom/memory"
)
```

## 故障排除

### 常见问题

#### Agent未被发现
- 检查Agent目录结构是否正确
- 确认Agent类名以`X`开头，以`Agent`结尾
- 检查Python文件语法错误

#### 任务执行失败
- 查看返回的错误信息
- 检查Agent的execute方法实现
- 确认任务描述清晰明确

#### 内存使用过高
- 定期清理短期记忆
- 调整记忆存储策略
- 监控任务执行日志

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from FreeLoop import AgentExecutor
executor = AgentExecutor()
result = executor.execute_task("调试任务")
```

## 性能优化

### 最佳实践
1. **Agent设计**: 保持Agent功能单一明确
2. **任务分解**: 将复杂任务分解为多个小任务
3. **缓存策略**: 合理使用记忆系统缓存结果
4. **错误处理**: 在Agent中实现完善的错误处理
5. **监控**: 定期查看任务状态和性能指标

### 扩展建议
- 添加Agent热重载功能
- 实现任务队列和异步执行
- 添加Web界面进行管理
- 集成更多外部服务

## 更新日志

### v1.0.0 (2025-08-03)
- ✨ 初始版本发布
- ✨ Agent自动发现和加载
- ✨ 任务规划和执行
- ✨ 记忆系统集成
- ✨ 实时任务跟踪
- ✨ 完整API接口

## 许可证

MIT License - 详见项目根目录LICENSE文件