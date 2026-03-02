#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meeting Agent - 會議管理 Agent
會議記錄、摘要、跟進
"""

import os
import json
from datetime import datetime, timedelta

class MeetingAgent:
    def __init__(self):
        self.data_path = os.path.expanduser("~/.openclaw/workspace/memory/meetings.json")
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"meetings": [], "actions": [], "templates": []}
    
    def save_data(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def add_meeting(self, title, participants, date=None, duration=60):
        """新增會議"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        meeting = {
            "id": f"meet_{len(self.data['meetings']) + 1}",
            "title": title,
            "participants": participants,
            "date": date,
            "duration": duration,
            "notes": "",
            "summary": "",
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        self.data["meetings"].append(meeting)
        self.save_data()
        
        return meeting
    
    def add_notes(self, meeting_id, notes):
        """添加會議記錄"""
        for meeting in self.data["meetings"]:
            if meeting["id"] == meeting_id:
                meeting["notes"] = notes
                meeting["updated_at"] = datetime.now().isoformat()
                self.save_data()
                return meeting
        return None
    
    def generate_summary(self, meeting_id):
        """生成摘要"""
        for meeting in self.data["meetings"]:
            if meeting["id"] == meeting_id:
                notes = meeting.get("notes", "")
                
                # 簡單摘要生成
                summary = f"會議：{meeting['title']}\n"
                summary += f"日期：{meeting['date']}\n"
                summary += f"參與者：{', '.join(meeting['participants'])}\n\n"
                
                if notes:
                    summary += f"記錄要點：\n{notes[:200]}..."
                
                meeting["summary"] = summary
                meeting["status"] = "completed"
                self.save_data()
                
                return summary
        return None
    
    def add_action(self, meeting_id, task, owner, due_date=None):
        """新增待辦事項"""
        action = {
            "id": f"act_{len(self.data['actions']) + 1}",
            "meeting_id": meeting_id,
            "task": task,
            "owner": owner,
            "due_date": due_date,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        self.data["actions"].append(action)
        self.save_data()
        
        return action
    
    def get_upcoming(self, days=7):
        """獲取即將到來的會議"""
        upcoming = []
        
        for meeting in self.data["meetings"]:
            if meeting["status"] == "scheduled":
                meeting_date = datetime.strptime(meeting["date"], "%Y-%m-%d %H:%M")
                
                if (meeting_date - datetime.now()).days <= days:
                    upcoming.append(meeting)
        
        return upcoming
    
    def get_pending_actions(self):
        """獲取待完成事項"""
        return [a for a in self.data["actions"] if a["status"] == "pending"]
    
    def mark_action_done(self, action_id):
        """標記完成"""
        for action in self.data["actions"]:
            if action["id"] == action_id:
                action["status"] = "completed"
                action["completed_at"] = datetime.now().isoformat()
                self.save_data()
                return action
        return None
    
    def run_analysis(self):
        """運行分析"""
        print("\n📅 Meeting Agent 分析")
        print("="*40)
        
        # 統計
        total = len(self.data["meetings"])
        completed = len([m for m in self.data["meetings"] if m["status"] == "completed"])
        scheduled = len([m for m in self.data["meetings"] if m["status"] == "scheduled"])
        
        print(f"\n📊 會議統計:")
        print(f"   總會議: {total}")
        print(f"   已完成: {completed}")
        print(f"   待舉行: {scheduled}")
        
        # 即將到來的會議
        upcoming = self.get_upcoming()
        if upcoming:
            print(f"\n📅 即將到來 ({len(upcoming)}):")
            for m in upcoming[:3]:
                print(f"   - {m['title']} ({m['date']})")
        
        # 待辦事項
        pending = self.get_pending_actions()
        if pending:
            print(f"\n⏳ 待辦事項 ({len(pending)}):")
            for a in pending[:3]:
                print(f"   - {a['task']} ({a['owner']})")
        
        return {
            "total": total,
            "completed": completed,
            "scheduled": scheduled,
            "upcoming": len(upcoming),
            "pending_actions": len(pending)
        }

if __name__ == "__main__":
    agent = MeetingAgent()
    
    # 添加測試會議
    agent.add_meeting(
        "BNI 週會",
        ["Joe", "Cynthia", "Team"],
        "2026-03-01 09:00",
        60
    )
    
    agent.add_meeting(
        "AI 系統檢討",
        ["Kira", "Evolution", "史萊姆"],
        "2026-03-02 14:00",
        45
    )
    
    # 添加待辦
    agent.add_action(
        "meet_1",
        "準備週會簡報",
        "Joe",
        "2026-02-28"
    )
    
    # 運行分析
    agent.run_analysis()
