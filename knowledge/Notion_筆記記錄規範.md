# 📋 Notion 筆記記錄規範

**建立日期：** 2026-02-18
**原因：** 曾經發生筆記內容空白問題

---

## ⚠️ 問題記錄

### 2026-02-18 事件

**問題：** 開發日誌頁面建立後內容空白

**原因：**
1. 第一次 API 請求格式錯誤
2. PATCH 請求只添加了標題區塊，沒有添加內容
3. 沒有驗證是否成功寫入

---

## ✅ 正確流程（必檢查）

### 1. 建立頁面
```bash
# 建立後立即檢查
curl .../pages | python3 -c "print(data['id'])"
```

### 2. 添加內容
```bash
# 添加後檢查區塊數
curl .../blocks/{id}/children | python3 -c "print(len(data['results']))"
```

### 3. 驗證清單

每次寫入 Notion 後必須檢查：
- [ ] 頁面 ID 是否取得
- [ ] 區塊數是否 > 0
- [ ] 內容是否正確顯示

---

## 🔧 修復方法

如果發現空白：
1. 查詢頁面區塊數：`GET /blocks/{id}/children`
2. 區塊數 = 0 → 重新添加內容
3. 使用 PATCH 重新寫入

---

## 📝 檢查腳本

```python
# 檢查頁面是否有內容
def check_notion_page(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)
    data = response.json()
    count = len(data.get('results', []))
    
    if count == 0:
        print("❌ 頁面空白！需要重新添加內容")
        return False
    else:
        print(f"✅ 頁面正常，有 {count} 個區塊")
        return True
```

---

*更新：2026-02-18*
