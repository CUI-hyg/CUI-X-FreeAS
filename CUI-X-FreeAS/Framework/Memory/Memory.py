import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

class MemorySystem:
    def __init__(self, memory_dir: str = None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        memory_dir = os.path.join(project_root, "Framework", "Memory", "data")
        self.memory_dir = memory_dir
        self.short_term_file = os.path.join(memory_dir, "short_term", "short_term.json")
        self.long_term_file = os.path.join(memory_dir, "long_term", "long_term.json")
        self.index_file = os.path.join(memory_dir, "index.json")
        os.makedirs(memory_dir, exist_ok=True)
        self.InitMemory()
        self.index = self.LoadIndex()
    
    def InitMemory(self):
        files = {
            self.short_term_file: {"memories": [], "last_updated": str(datetime.now())},
            self.long_term_file: {"memories": [], "last_updated": str(datetime.now())},
            self.index_file: {"index": {"short_term": {}, "long_term": {}}}
        }
        for file_path, default_content in files.items():
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(default_content, f, ensure_ascii=False, indent=2)
                    print(f"Memory文件已创建/修复: {file_path}")
                else:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        if file_path.endswith('long_term.json') or file_path.endswith('short_term.json'):
                            if "memories" not in data:
                                data = {"memories": [], "last_updated": str(datetime.now())}
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, ensure_ascii=False, indent=2)
                                print(f"Memory文件结构已修复: {file_path}")
                    except json.JSONDecodeError:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(default_content, f, ensure_ascii=False, indent=2)
                        print(f"Memory文件已重新创建: {file_path}")
            except Exception as e:
                print(f"创建Memory文件失败 {file_path}: {e}")
    
    def LoadIndex(self) -> Dict[str, Any]:
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("index", {})
        except Exception as e:
            print(f"加载索引文件失败: {e}")
            return {}
    
    def IndexSaver(self):
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump({"index": self.index, "last_updated": str(datetime.now())}, 
                         f, ensure_ascii=False, indent=2)
            return "索引保存成功"
        except Exception as e:
            print(f"保存索引失败: {e}")
            return f"索引保存失败: {e}"
    
    def MemIDCreator(self, content: str) -> str:
        content_hash = hashlib.md5(content.encode()).hexdigest()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{timestamp}_{content_hash[:8]}"
    
    def IndexUpdater(self, memory_id: str, memory_type: str, keywords: List[str], content: str):
        for keyword in keywords:
            keyword = keyword.lower()
            if keyword not in self.index:
                self.index[keyword] = []
            memory_entry = {
                "id": memory_id,
                "type": memory_type,
                "content_preview": content[:50] + "..." if len(content) > 50 else content,
                "timestamp": str(datetime.now())
            }
            existing = next((item for item in self.index[keyword] 
                           if item["id"] == memory_id), None)
            if not existing:
                self.index[keyword].append(memory_entry)
                self.index[keyword].sort(key=lambda x: x["timestamp"], reverse=True)
        self.IndexSaver()
    
    def st_mem_add(self, content: str, keywords: List[str] = None) -> str:
        """短期记忆"""
        try:
            memory_id = self.MemIDCreator(content)
            keywords = keywords or []
            memory = {
                "id": memory_id,
                "content": content,
                "keywords": keywords,
                "timestamp": str(datetime.now()),
                "type": "short_term"
            }
            with open(self.short_term_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data["memories"].append(memory)
            data["last_updated"] = str(datetime.now())
            with open(self.short_term_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.IndexUpdater(memory_id, "short_term", keywords, content)
            print(f"短期记忆已保存: {memory_id}")
            return memory_id
        except Exception as e:
            print(f"保存短期记忆失败: {e}")
            raise e
    
    def lt_mem_add(self, content: str, keywords: List[str] = None, importance: int = 5) -> str:
        try:
            memory_id = self.MemIDCreator(content)
            keywords = keywords or []
            memory = {
                "id": memory_id,
                "content": content,
                "keywords": keywords,
                "importance": importance,
                "timestamp": str(datetime.now()),
                "type": "long_term"
            }
            with open(self.long_term_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data["memories"].append(memory)
            data["last_updated"] = str(datetime.now())
            with open(self.long_term_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.IndexUpdater(memory_id, "long_term", keywords, content)
            print(f"长期记忆已保存: {memory_id}")
            return memory_id
        except Exception as e:
            print(f"保存长期记忆失败: {e}")
            raise e
    
    def search_mem(self, query: str, memory_type: str = "all") -> List[Dict[str, Any]]:
        query = query.lower()
        results = []
        matching_ids = set()
        for keyword, memories in self.index.items():
            if query in keyword:
                for memory_ref in memories:
                    if memory_type == "all" or memory_ref["type"] == memory_type:
                        matching_ids.add(memory_ref["id"])
        if memory_type in ["all", "short_term"]:
            results.extend(self.get_mem_ids(matching_ids, "short_term"))
        if memory_type in ["all", "long_term"]:
            results.extend(self.get_mem_ids(matching_ids, "long_term"))
        if not results:
            results.extend(self.content_search(query, memory_type))
        results.sort(key=lambda x: x["timestamp"], reverse=True)
        return results
    
    def get_mem_ids(self, memory_ids: set, memory_type: str) -> List[Dict[str, Any]]:
        results = []
        file_path = self.short_term_file if memory_type == "short_term" else self.long_term_file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for memory in data["memories"]:
                    if memory["id"] in memory_ids:
                        results.append(memory)
        except Exception:
            pass
        return results
    
    def content_search(self, query: str, memory_type: str) -> List[Dict[str, Any]]:
        results = []
        if memory_type in ["all", "short_term"]:
            results.extend(self.file_search(query, self.short_term_file))
        if memory_type in ["all", "long_term"]:
            results.extend(self.file_search(query, self.long_term_file))
        return results
    
    def file_search(self, query: str, file_path: str) -> List[Dict[str, Any]]:
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for memory in data["memories"]:
                    if query in memory["content"].lower() or \
                       any(query in str(kw).lower() for kw in memory.get("keywords", [])):
                        results.append(memory)
        except Exception:
            pass
        return results
    
    def get_all_mem(self, memory_type: str = "all") -> List[Dict[str, Any]]:
        results = []
        if memory_type in ["all", "short_term"]:
            try:
                with open(self.short_term_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    results.extend(data["memories"])
            except Exception:
                pass
        if memory_type in ["all", "long_term"]:
            try:
                with open(self.long_term_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    results.extend(data["memories"])
            except Exception:
                pass
        return results
    
    def del_mem(self, memory_id: str) -> bool:
        deleted = False
        if self.del_file(memory_id, self.short_term_file):
            deleted = True
        if self.del_file(memory_id, self.long_term_file):
            deleted = True
        self.remove_index(memory_id)
        return deleted
    
    def del_file(self, memory_id: str, file_path: str) -> bool:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            original_count = len(data["memories"])
            data["memories"] = [m for m in data["memories"] if m["id"] != memory_id]
            if len(data["memories"]) < original_count:
                data["last_updated"] = str(datetime.now())
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
        except Exception:
            pass
        return False
    
    def remove_index(self, memory_id: str):
        for keyword in list(self.index.keys()):
            self.index[keyword] = [item for item in self.index[keyword] 
                                 if item["id"] != memory_id]
            if not self.index[keyword]:
                del self.index[keyword]
        self.IndexSaver()
    
    def clean_sm(self):
        try:
            with open(self.short_term_file, 'w', encoding='utf-8') as f:
                json.dump({"memories": [], "last_updated": str(datetime.now())}, 
                         f, ensure_ascii=False, indent=2)
            self.recreate_index()
            print("短期记忆已清空")
        except Exception as e:
            print(f"清空短期记忆失败: {e}")
            raise e
    
    def recreate_index(self):
        try:
            self.index = {}
            with open(self.short_term_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for memory in data.get("memories", []):
                self.IndexUpdater(memory["id"], "short_term", 
                                memory.get("keywords", []), memory["content"])
            with open(self.long_term_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for memory in data.get("memories", []):
                self.IndexUpdater(memory["id"], "long_term", 
                                memory.get("keywords", []), memory["content"])
            self.IndexSaver()
            print("索引已重新创建")
        except Exception as e:
            print(f"重新创建索引失败: {e}")
            raise e