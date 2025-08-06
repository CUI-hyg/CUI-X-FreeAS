# CUIX-HiOS 记忆系统

## 概述

CUIX-HiOS记忆系统是一个多智能体协作的记忆管理模块，支持短期和长期记忆的分离存储，提供高效的索引搜索功能。

## 特性

- **双重记忆存储**：短期记忆和长期记忆分别存储
- **智能索引**：基于关键词的快速搜索
- **API接口**：简洁易用的接口供其他模块调用
- **JSON存储**：使用JSON格式存储，易于查看和调试
- **时间戳管理**：记录每条记忆的创建时间
- **重要性标记**：长期记忆支持重要性等级

## 文件结构

```
Framework/Memory/
├── memory_system.py    # 核心记忆系统实现
├── __init__.py        # 模块接口
├── example_usage.py   # 使用示例
├── data/              # 存储目录
│   ├── short_term_memory.json   # 短期记忆存储
│   ├── long_term_memory.json    # 长期记忆存储
│   └── memory_index.json        # 记忆索引
└── README.md          # 本文档
```

## 使用方法

### 1. 基础使用

```python
from Framework.Memory import memory_system

# 添加短期记忆
short_id = memory_system.add_short_term_memory(
    "用户询问明天的天气",
    keywords=["天气", "明天", "用户"]
)

# 添加长期记忆  
long_id = memory_system.add_long_term_memory(
    "用户偏好：喜欢晴天",
    keywords=["用户偏好", "天气", "晴天"],
    importance=8
)

# 搜索记忆
results = memory_system.search_memories("天气")
print(f"找到 {len(results)} 条相关记忆")

# 获取所有记忆
all_memories = memory_system.get_all_memories()
short_memories = memory_system.get_all_memories("short_term")
long_memories = memory_system.get_all_memories("long_term")
```

### 2. 简化API

```python
from Framework.Memory import (
    add_short_memory, add_long_memory, 
    search_memory, get_memories, delete_memory
)

# 添加记忆
short_id = add_short_memory("短期记忆内容", ["关键词"])
long_id = add_long_memory("长期记忆内容", ["关键词"], importance=7)

# 搜索和获取
results = search_memory("搜索词")
memories = get_memories("short_term")  # 或 "long_term", "all"

# 删除记忆
success = delete_memory(memory_id)
```

### 3. 高级功能

#### 记忆搜索
```python
# 搜索所有记忆
all_results = memory_system.search_memories("关键词")

# 仅搜索短期记忆
short_results = memory_system.search_memories("关键词", memory_type="short_term")

# 仅搜索长期记忆  
long_results = memory_system.search_memories("关键词", memory_type="long_term")
```

#### 记忆管理
```python
# 删除特定记忆
memory_system.delete_memory("memory_id_here")

# 清空短期记忆
memory_system.clear_short_term_memory()

# 重建索引（数据异常时使用）
memory_system._rebuild_index()
```

## API参考

### MemorySystem类

#### 添加记忆
- `add_short_term_memory(content, keywords=None) -> str`
- `add_long_term_memory(content, keywords=None, importance=5) -> str`

#### 搜索记忆
- `search_memories(query, memory_type="all") -> List[Dict]`
- `get_all_memories(memory_type="all") -> List[Dict]`

#### 管理记忆
- `delete_memory(memory_id) -> bool`
- `clear_short_term_memory()`

### 记忆数据结构

#### 短期记忆
```json
{
  "id": "时间戳_hash",
  "content": "记忆内容",
  "keywords": ["关键词1", "关键词2"],
  "timestamp": "创建时间",
  "type": "short_term"
}
```

#### 长期记忆
```json
{
  "id": "时间戳_hash", 
  "content": "记忆内容",
  "keywords": ["关键词1", "关键词2"],
  "importance": 1-10,
  "timestamp": "创建时间",
  "type": "long_term"
}
```

## 集成指南

### 在Agent中使用

```python
from Framework.Memory import add_short_memory, search_memory

class MyAgent:
    def process_message(self, message):
        # 添加用户输入到短期记忆
        add_short_memory(f"用户说: {message}", ["用户输入"])
        
        # 搜索相关记忆
        related = search_memory(message)
        
        # 根据记忆生成响应
        # ... 处理逻辑 ...
        
        # 添加响应到记忆
        add_short_memory(f"助手回复: {response}", ["助手回复"])
```

### 数据持久化

记忆数据存储在 `Framework/Memory/data/` 目录下：
- `short_term_memory.json` - 短期记忆
- `long_term_memory.json` - 长期记忆  
- `memory_index.json` - 搜索索引

## 注意事项

1. **关键词选择**：建议使用有意义的关键词，便于搜索
2. **重要性等级**：长期记忆的importance范围1-10，数值越高越重要
3. **定期清理**：短期记忆可定期清理，长期记忆保留重要信息
4. **索引重建**：如遇到搜索异常，可调用 `_rebuild_index()` 重建索引

## 故障排除

### 常见问题

1. **搜索不到记忆**：检查关键词是否正确，尝试重建索引
2. **文件权限错误**：确保有写入 `Framework/Memory/data/` 目录的权限
3. **JSON格式错误**：手动检查JSON文件格式，或删除重建

### 调试方法

```python
# 查看所有记忆
print(memory_system.get_all_memories())

# 查看索引
print(memory_system.index.keys())

# 检查特定文件
import json
with open('Framework/Memory/data/short_term_memory.json') as f:
    print(json.load(f))
```