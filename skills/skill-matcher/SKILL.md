# Skill Matcher Skill

## 功能
根據任務需求，自動匹配最適合的 Skills 和 Agents。

## 匹配邏輯

1. **接收任務描述**
2. **提取關鍵詞**
3. **匹配 Skills**
4. **選擇最佳 Agent**
5. **執行並回報**

## 技能領域

| 領域 | 可用 Skills |
|------|-------------|
| Coding | coding, development, debugging |
| Writing | copywriting, content, editing |
| Design | ui-design, graphic, ux |
| Analysis | data, analytics, research |
| Knowledge | memory, learning, RAG |
| Governance | decision, policy, ethics |

## 匹配優先級

1. 精確匹配 > 模糊匹配
2. 有 Skills > 無 Skills
3. 主模型可用 > 備用模型

---
*更新：2026-03-01*
