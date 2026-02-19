# TOOLS.md - model-dispatcher Tools

## 模型 API

### Ollama (本地)

- **端點**: http://localhost:11434
- **模型**: llama3:latest
- **用途**: 簡單/中等任務

### MiniMax (雲端)

- **端點**: MiniMax API
- **模型**: abab 6.5+
- **用途**: 複雜任務

---

## 調度命令

### 選擇模型

```bash
# 檢查 Ollama 狀態
ollama list

# 測試回應時間
time ollama generate --prompt "test"
```

### 上下文傳遞

```python
# 打包上下文
context = {
    "task": "...",
    "memories": [...],
    "history": [...]
}
```

---

## 日誌

- 記錄每次模型選擇
- 記錄輸出品質
- 用於優化決策
