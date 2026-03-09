#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記憶統計報告 - Memory Statistics Report
每月產出使用報告
"""

import os
import json
import glob
from datetime import datetime, timedelta

class MemoryStatsReport:
    def __init__(self):
        self.base_path = os.path.expanduser("~/.openclaw/workspace/memory/")
        self.report_file = os.path.join(self.base_path, "memory_stats_report.json")
    
    def generate_report(self):
        """生成報告"""
        print("\n📊 記憶統計報告")
        print("="*50)
        
        # 1. 總體統計
        md_files = glob.glob(os.path.join(self.base_path, "*.md"))
        md_files = [f for f in md_files if not os.path.basename(f).startswith(".")]
        
        total_size = sum(os.path.getsize(f) for f in md_files)
        
        # 2. 日期範圍
        dates = []
        for f in md_files:
            name = os.path.basename(f)
            if "2026-" in name:
                dates.append(name[:10])
        
        # 3. 類別統計
        categories = {}
        for f in md_files:
            name = os.path.basename(f).lower()
            
            if "learning" in name or "study" in name:
                cat = "learning"
            elif "marketing" in name or "trend" in name:
                cat = "marketing"
            elif "agent" in name or "evolution" in name:
                cat = "agent"
            elif "daily" in name:
                cat = "daily"
            elif "notion" in name:
                cat = "notion"
            else:
                cat = "other"
            
            categories[cat] = categories.get(cat, 0) + 1
        
        # 4. 最近活動
        recent = sorted(md_files, key=os.path.getmtime, reverse=True)[:10]
        
        # 5. 大小分布
        size_ranges = {
            "<1KB": 0,
            "1-5KB": 0,
            "5-10KB": 0,
            ">10KB": 0
        }
        
        for f in md_files:
            size = os.path.getsize(f)
            if size < 1024:
                size_ranges["<1KB"] += 1
            elif size < 5*1024:
                size_ranges["1-5KB"] += 1
            elif size < 10*1024:
                size_ranges["5-10KB"] += 1
            else:
                size_ranges[">10KB"] += 1
        
        # 組裝報告
        report = {
            "generated_at": datetime.now().isoformat(),
            "period": {
                "start": min(dates) if dates else None,
                "end": max(dates) if dates else None
            },
            "total_files": len(md_files),
            "total_size_kb": round(total_size / 1024, 2),
            "categories": categories,
            "size_distribution": size_ranges,
            "recent_files": [os.path.basename(f) for f in recent]
        }
        
        # 儲存
        with open(self.report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        # 輸出
        print(f"\n📅 期間: {report['period']['start']} ~ {report['period']['end']}")
        print(f"📁 總檔案: {report['total_files']}")
        print(f"💾 總大小: {report['total_size_kb']} KB")
        
        print(f"\n📂 類別分布:")
        for cat, count in sorted(report["categories"].items(), key=lambda x: x[1], reverse=True):
            print(f"   {cat}: {count}")
        
        print(f"\n📊 大小分布:")
        for range_, count in report["size_distribution"].items():
            print(f"   {range_}: {count}")
        
        print(f"\n🆕 最近檔案:")
        for f in report["recent_files"][:5]:
            print(f"   - {f}")
        
        print(f"\n✅ 報告已儲存: {self.report_file}")
        
        return report

if __name__ == "__main__":
    report = MemoryStatsReport()
    report.generate_report()
