# 錯誤學習記錄 - 2026-03-04

## 時間
2026-03-04 07:07

## 錯誤類型
1. **Gateway 頻繁關閉** - node.err.log 顯示多次 "node host gateway closed (1006)" 和 "node host gateway closed (1012): service restart"
2. **Config Invalid** - node.log 顯示 "Config invalid; doctor will run with best-effort config"
3. **Cron Job Skipped** - 多个 job 因 "main job requires payload.kind=\"systemEvent\"" 被跳過

## 錯誤詳情
- Gateway 持續崩潰後自動重啟 (1006 = abnormal closure, 1012 = service restart)
- Config 加載有問題但以 best-effort 模式運行
- Cron jobs 配置問題導致跳過

## 影響
- Gateway 進程存在但 API 響應異常
- 定時任務部分失敗

## 學習/改進
- 需要檢查 openclaw.json 配置
- 需要修復 cron job payload 配置
- Gateway 穩定性需關注
