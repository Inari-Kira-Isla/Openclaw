#!/usr/bin/env python3
"""
記憶主題聚類腳本
分析記憶文件，識別主題並建立聚類
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
OUTPUT_FILE = MEMORY_DIR / "2026-03-05-topic-clustering.md"

# 主題關鍵字映射
TOPIC_KEYWORDS = {
    "OpenClaw 監控": ["監控", "monitor", "heartbeat", "agent", "調度", "健康檢查"],
    "AI 趨勢研究": ["Hacker News", "AI", "趨勢", "research", "trending", "衝突型"],
    "代碼開發": ["代碼", "開發", "coding", "git", "commit", "PR", "feature"],
    "系統優化": ["優化", "optimization", "performance", "token", "記憶", "效率"],
    "安全審計": ["安全", "security", "審計", "firewall", "SSL", "漏洞"],
    "工作流程": ["workflow", "自動化", "automation", "n8n", "cron", "排程"],
    "知識管理": ["知識", "knowledge", "FAQ", "memory", "向量", "RAG"],
    "商業應用": ["BNI", "商業", "marketing", "客戶", "reminder", "供應鏈"],
    "錯誤處理": ["error", "錯誤", "bug", "fix", "故障", "emergency"],
    "反饋分析": ["反饋", "feedback", "分析", "report", "評估"]
}

def extract_topics(content):
    """從內容中提取主題"""
    topics = []
    content_lower = content.lower()
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in content_lower:
                topics.append(topic)
                break
    
    return topics if topics else ["其他"]

def get_memory_age(filename):
    """獲取記憶的時間戳"""
    try:
        # 從文件名提取日期
        match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
        if match:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        
        # 嘗試從文件修改時間
        mtime = os.path.getmtime(filename)
        return datetime.fromtimestamp(mtime)
    except:
        return datetime.now()

def analyze_memories():
    """分析所有記憶並建立聚類"""
    memory_files = list(MEMORY_DIR.glob("*.md"))
    
    # 排除特殊文件
    exclude_files = ["MEMORY.md", "SOUL.md", "AGENTS.md", "USER.md", "TOOLS.md"]
    memory_files = [f for f in memory_files if f.name not in exclude_files]
    
    # 按主題分組
    topic_clusters = defaultdict(list)
    total_count = 0
    
    for mem_file in memory_files:
        try:
            content = mem_file.read_text(encoding='utf-8', errors='ignore')
            topics = extract_topics(content)
            
            # 計算權重（最近的文件權重更高）
            age = get_memory_age(mem_file)
            days_old = (datetime.now() - age).days
            weight = max(1, 10 - days_old // 7)  # 一週內的權重較高
            
            for topic in topics:
                topic_clusters[topic].append({
                    "file": mem_file.name,
                    "weight": weight,
                    "age_days": days_old
                })
            
            total_count += 1
        except Exception as e:
            print(f"Error processing {mem_file.name}: {e}")
    
    return topic_clusters, total_count

def generate_report(topic_clusters, total_count):
    """生成聚類報告"""
    report = f"""# 📊 記憶主題聚類報告

生成時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 總覽

- 總記憶數：{total_count}
- 識別主題數：{len(topic_clusters)}

---

"""
    # 按記憶數量排序主題
    sorted_topics = sorted(topic_clusters.items(), 
                          key=lambda x: len(x[1]), 
                          reverse=True)
    
    for topic, memories in sorted_topics:
        # 按權重排序
        sorted_memories = sorted(memories, key=lambda x: x["weight"], reverse=True)
        
        report += f"## {topic} ({len(memories)}則)\n\n"
        
        # 顯示前5個最相關的記憶
        for mem in sorted_memories[:5]:
            age_str = f"{mem['age_days']}天前" if mem['age_days'] > 0 else "今天"
            report += f"- {mem['file']} ({age_str})\n"
        
        if len(memories) > 5:
            report += f"- ...還有 {len(memories) - 5} 則\n"
        
        report += "\n"
    
    return report

if __name__ == "__main__":
    print("開始記憶主題聚類分析...")
    
    topic_clusters, total_count = analyze_memories()
    report = generate_report(topic_clusters, total_count)
    
    # 寫入報告
    OUTPUT_FILE.write_text(report, encoding='utf-8')
    
    print(f"✅ 聚類完成！")
    print(f"   總記憶數：{total_count}")
    print(f"   識別主題：{len(topic_clusters)}")
    print(f"   報告位置：{OUTPUT_FILE}")
