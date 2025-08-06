import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading
from dataclasses import dataclass

@dataclass
class TaskEvent:
    task_id: str
    event_type: str  # start, progress, complete, warning这几类
    timestamp: datetime
    data: Dict[str, Any]

class TaskMonitor:
    def __init__(self, planner_dir: str):
        self.planner_dir = planner_dir
        self.events_file = os.path.join(planner_dir, "task_events.json")
        self.monitor_file = os.path.join(planner_dir, "monitor_status.json")
        self.observers: List[callable] = []
        self.running = False
        self.monitor_thread = None
        self._init_monitor()
    
    def _init_monitor(self):
        if not os.path.exists(self.events_file):
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump({"events": []}, f, ensure_ascii=False, indent=2)
        if not os.path.exists(self.monitor_file):
            with open(self.monitor_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "status": "stopped",
                    "last_check": str(datetime.now()),
                    "active_alerts": []
                }, f, ensure_ascii=False, indent=2)
    
    def add_observer(self, callback: callable):
        """添加事件观察者"""
        self.observers.append(callback)
    
    def remove_observer(self, callback: callable):
        """移除事件观察者"""
        if callback in self.observers:
            self.observers.remove(callback)
    
    def _notify_observers(self, event: TaskEvent):
        """通知所有观察者"""
        for callback in self.observers:
            try:
                callback(event)
            except Exception as e:
                print(f"观察者回调错误: {e}")
    
    def _load_events(self) -> List[Dict]:
        """加载事件历史"""
        try:
            with open(self.events_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("events", [])
        except Exception:
            return []
    
    def _save_event(self, event: TaskEvent):
        """保存事件"""
        events = self._load_events()
        event_data = {
            "task_id": event.task_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
            "data": event.data
        }
        events.append(event_data)
        if len(events) > 1000:
            events = events[-1000:]
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump({"events": events}, f, ensure_ascii=False, indent=2)
    
    def log_event(self, task_id: str, event_type: str, data: Dict[str, Any]):
        """记录任务事件"""
        event = TaskEvent(task_id, event_type, datetime.now(), data)
        self._save_event(event)
        self._notify_observers(event)
    
    def start_monitoring(self, interval_seconds: int = 30):
        if self.running:
            return
        self.running = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(interval_seconds,)
        )
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        self._update_monitor_status("running")
        self.log_event("system", "monitor_start", {
            "interval": interval_seconds,
            "message": "任务监控已启动"
        })
    
    def stop_monitoring(self):
        """停止实时监控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self._update_monitor_status("stopped")
        self.log_event("system", "monitor_stop", {
            "message": "任务监控已停止"
        })
    
    def _update_monitor_status(self, status: str):
        try:
            with open(self.monitor_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "status": status,
                    "last_check": str(datetime.now()),
                    "active_alerts": self._get_active_alerts()
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _monitor_loop(self, interval_seconds: int):
        while self.running:
            try:
                self._check_tasks()
                time.sleep(interval_seconds)
            except Exception as e:
                self.log_event("system", "error", {
                    "error": str(e),
                    "message": "监控循环异常"
                })
                time.sleep(interval_seconds)
    
    def _check_tasks(self):
        tracker_file = os.path.join(self.planner_dir, "task_tracker.json")
        try:
            with open(tracker_file, 'r', encoding='utf-8') as f:
                tracker = json.load(f)
            active_tasks = tracker.get("active_tasks", {})
            for task_id, task in active_tasks.items():
                self._check_task_deadlines(task_id, task)
                self._check_task_progress(task_id, task)
        except FileNotFoundError:
            pass
    
    def _check_task_deadlines(self, task_id: str, task: Dict):
        if "deadline" in task and task["deadline"]:
            try:
                deadline = datetime.fromisoformat(task["deadline"])
                now = datetime.now()
                if deadline < now:
                    self.log_event(task_id, "deadline_warning", {
                        "message": "任务已逾期",
                        "deadline": task["deadline"],
                        "overdue_hours": (now - deadline).total_seconds() / 3600
                    })
                elif deadline - now < timedelta(hours=24):
                    self.log_event(task_id, "deadline_approaching", {
                        "message": "任务即将到期",
                        "hours_remaining": (deadline - now).total_seconds() / 3600
                    })
            except ValueError:
                pass
    
    def _check_task_progress(self, task_id: str, task: Dict):
        progress = task.get("progress", 0)
        estimated_hours = task.get("estimated_hours", 1)
        start_time = datetime.fromisoformat(task["start_time"])
        elapsed_hours = (datetime.now() - start_time).total_seconds() / 3600
        expected_progress = min(100, (elapsed_hours / estimated_hours) * 100)
        if progress < expected_progress - 20:
            self.log_event(task_id, "progress_warning", {
                "message": "任务进度落后",
                "current_progress": progress,
                "expected_progress": expected_progress,
                "elapsed_hours": elapsed_hours
            })
    
    def _get_active_alerts(self) -> List[Dict]:
        alerts = []
        events = self._load_events()
        cutoff_time = datetime.now() - timedelta(hours=24)
        for event in events:
            event_time = datetime.fromisoformat(event["timestamp"])
            if event_time > cutoff_time and "warning" in event["event_type"]:
                alerts.append(event)
        return alerts[-10:] 
    
    def get_monitor_status(self) -> Dict[str, Any]:
        try:
            with open(self.monitor_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"status": "error", "last_check": str(datetime.now())}
    
    def get_recent_events(self, task_id: str = None, limit: int = 10) -> List[Dict]:
        events = self._load_events()
        if task_id:
            events = [e for e in events if e["task_id"] == task_id]
        events.sort(key=lambda x: x["timestamp"], reverse=True)
        return events[:limit]
    
    def get_task_analytics(self, task_id: str) -> Dict[str, Any]:
        events = self._load_events()
        task_events = [e for e in events if e["task_id"] == task_id]
        if not task_events:
            return {}
        start_events = [e for e in task_events if e["event_type"] == "start"]
        progress_events = [e for e in task_events if e["event_type"] == "progress"]
        complete_events = [e for e in task_events if e["event_type"] == "complete"]
        analytics = {
            "total_events": len(task_events),
            "start_time": start_events[0]["timestamp"] if start_events else None,
            "completion_time": complete_events[0]["timestamp"] if complete_events else None,
            "progress_updates": len(progress_events),
            "warnings": len([e for e in task_events if "warning" in e["event_type"]]),
            "events": task_events
        }
        return analytics