#!/usr/bin/env python3
"""
RAG Vector Expansion Script
向量庫擴展：從記憶檔案生成更多向量
"""

import json
import os
import hashlib
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw/workspace"
VECTORS_FILE = WORKSPACE / "memory/vectors/vectors.json"

def load_existing_vectors():
    """載入現有向量庫"""
    if VECTORS_FILE.exists():
        with open(VECTORS_FILE) as f:
            return json.load(f)
    return {"version": "1.0", "created": "2026-03-01", "documents": []}

def save_vectors(data):
    """儲存向量庫"""
    with open(VECTORS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def chunk_text(text, chunk_size=500):
    """將文本分塊"""
    # 簡單按段落分塊
    paragraphs = text.split('\n\n')
    chunks = []
    current = ""
    
    for para in paragraphs:
        if len(current) + len(para) < chunk_size:
            current += para + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            current = para + "\n\n"
    
    if current:
        chunks.append(current.strip())
    
    return chunks

def generate_vector_id(text):
    """生成向量ID"""
    return hashlib.md5(text.encode()).hexdigest()[:16]

def vectorize_memory_files():
    """向量化記憶檔案"""
    data = load_existing_vectors()
    existing_sources = {doc['source'] for doc in data['documents']}
    
    print(f"現有向量: {len(data['documents'])}")
    
    # 獲取所有記憶檔案
    memory_dir = WORKSPACE / "memory"
    md_files = list(memory_dir.glob("*.md"))
    
    new_docs = []
    
    for md_file in md_files:
        if md_file.name in existing_sources:
            continue
            
        try:
            content = md_file.read_text(encoding='utf-8')
            chunks = chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                if len(chunk) < 50:  # 跳過太短的片段
                    continue
                    
                doc = {
                    "type": "memory_chunk",
                    "source": md_file.name,
                    "chunk_id": i,
                    "title": chunk[:100],
                    "content": chunk[:500]
                }
                new_docs.append(doc)
                
        except Exception as e:
            print(f"錯誤: {md_file.name} - {e}")
    
    print(f"新增向量: {len(new_docs)}")
    data['documents'].extend(new_docs)
    save_vectors(data)
    
    return len(new_docs)

def vectorize_skills():
    """向量化Skills文檔"""
    data = load_existing_vectors()
    skills_dir = WORKSPACE / "skills"
    
    new_docs = []
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('_'):
            continue
            
        # 查找 SKILL.md
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            try:
                content = skill_md.read_text(encoding='utf-8')
                chunks = chunk_text(content)
                
                for i, chunk in enumerate(chunks):
                    if len(chunk) < 50:
                        continue
                    doc = {
                        "type": "skill",
                        "source": f"skill-{skill_dir.name}",
                        "chunk_id": i,
                        "title": chunk[:100],
                        "content": chunk[:500]
                    }
                    new_docs.append(doc)
            except Exception as e:
                print(f"Skill錯誤: {skill_dir.name} - {e}")
    
    print(f"Skills 新增: {len(new_docs)}")
    data['documents'].extend(new_docs)
    save_vectors(data)
    
    return len(new_docs)

if __name__ == "__main__":
    print("=== RAG 向量擴展 ===")
    
    count1 = vectorize_memory_files()
    count2 = vectorize_skills()
    
    data = load_existing_vectors()
    print(f"\n總向量: {len(data['documents'])}")
    print(f"目標: >1000")
