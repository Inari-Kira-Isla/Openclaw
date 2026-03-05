# OpenClaw + ComfyUI 整合計劃

**日期**: 2026-02-20

---

## 目標

讓 OpenClaw 可以透過指令生成 AI 影片

---

## 架構

```
OpenClaw (Telegram)
       ↓
   n8n Workflow
       ↓
 ComfyUI API
       ↓
   生成影片
       ↓
   回傳 Telegram
```

---

## 實現方式

### 1. ComfyUI API

```bash
# ComfyUI 預設端口
COMFYUI_HOST=http://localhost:8188
```

### 2. Workflow

```
Telegram Message
       ↓
   n8n - 解析指令
       ↓
 ComfyUI - 執行生成
       ↓
 n8n - 下載影片
       ↓
 Telegram - 回傳
```

---

## ComfyUI API 端點

| 端點 | 功能 |
|------|------|
| `/prompt` | 提交生成任務 |
| `/history` | 查詢狀態 |
| `/history/{prompt_id}` | 取得結果 |

---

## Prompt 格式

```json
{
  "prompt": {
    "3": {
      "inputs": {
        "text": "aliens emerged from a UFO",
        "seed": 42
      },
      "class_type": "Text To Video"
    }
  }
}
```

---

## 實施步驟

1. [ ] 安裝 ComfyUI
2. [ ] 設定 API
3. [ ] 建立 n8n Workflow
4. [ ] 測試生成

---

## 相關檔案

- `memory/comfyui-video-generation.md`
- `~/Desktop/n8n_workflows/comfyui-video.json` (待建立)

---
