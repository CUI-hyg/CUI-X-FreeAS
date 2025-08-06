import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Framework.Memory import Memory

def demo_Memory():
    print("=== CUIX-HiOS 记忆系统演示 ===\n")
    # 1. 添加短期记忆
    print("1. 添加短期记忆...")
    short_id1 = Memory.add_short_term_memory(
        "用户询问天气情况，需要明天下午3点的天气预报",
        keywords=["天气", "用户询问", "明天", "下午3点"]
    )
    short_id2 = Memory.add_short_term_memory(
        "当前对话主题：旅行计划",
        keywords=["对话主题", "旅行", "计划"]
    )
    print(f"添加短期记忆ID: {short_id1}")
    print(f"添加短期记忆ID: {short_id2}")
    # 2. 添加长期记忆
    print("\n2. 添加长期记忆...")
    long_id1 = Memory.add_long_term_memory(
        "用户偏好：喜欢温暖的天气，不喜欢下雨天",
        keywords=["用户偏好", "天气", "喜好"],
        importance=8
    )
    long_id2 = Memory.add_long_term_memory(
        "用户常用地点：北京、上海、深圳",
        keywords=["常用地点", "北京", "上海", "深圳"],
        importance=9
    )
    print(f"添加长期记忆ID: {long_id1}")
    print(f"添加长期记忆ID: {long_id2}")
    # 3. 搜索记忆
    print("\n3. 搜索记忆...")
    # 搜索天气相关记忆
    weather_results = Memory.search_memories("天气")
    print(f"搜索'天气'相关记忆: {len(weather_results)}条")
    for result in weather_results:
        print(f"  - {result['type']}: {result['content'][:50]}...")
    # 搜索用户相关记忆
    user_results = Memory.search_memories("用户")
    print(f"搜索'用户'相关记忆: {len(user_results)}条")
    # 4. 获取所有记忆
    print("\n4. 获取所有记忆...")
    all_memories = Memory.get_all_memories()
    short_memories = Memory.get_all_memories("short_term")
    long_memories = Memory.get_all_memories("long_term")
    print(f"总记忆数: {len(all_memories)}")
    print(f"短期记忆数: {len(short_memories)}")
    print(f"长期记忆数: {len(long_memories)}")
    # 5. 删除记忆示例
    print("\n5. 删除记忆示例...")
    # 这里不实际删除，仅展示接口
    print("删除接口: Memory.delete_memory(memory_id)")
    # 6. 清空短期记忆示例
    print("\n6. 清空短期记忆接口...")
    print("清空接口: Memory.clean_sm()")
    print("\n=== 演示完成 ===")

def demo_simple_api():
    """演示简化API的使用"""
    print("\n=== 简化API演示 ===\n")
    from Framework.Memory import (
        add_short_memory, add_long_memory, search_memory, 
        get_memories, delete_memory
    )
    # 使用简化API
    print("使用简化API添加记忆...")
    short_id = add_short_memory("这是一个测试记忆", ["测试"])
    long_id = add_long_memory("这是一个重要的长期记忆", ["重要", "测试"], importance=7)
    print(f"简化API添加短期记忆ID: {short_id}")
    print(f"简化API添加长期记忆ID: {long_id}")
    # 搜索
    results = search_memory("测试")
    print(f"简化API搜索结果: {len(results)}条")

if __name__ == "__main__":
    demo_Memory()
    demo_simple_api()