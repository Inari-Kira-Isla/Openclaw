#!/bin/bash
set -uo pipefail

# ============================================================
# cron_cleanup.sh — Disable duplicate and problematic cron jobs
# Usage: ./cron_cleanup.sh              (dry-run, shows what would happen)
#        ./cron_cleanup.sh --execute    (actually disables the jobs)
# ============================================================

EXECUTE=false
DISABLED_COUNT=0

if [[ "${1:-}" == "--execute" ]]; then
  EXECUTE=true
  echo "=== EXECUTE MODE: Will disable jobs for real ==="
else
  echo "=== DRY-RUN MODE: Pass --execute to actually disable ==="
fi
echo ""

disable_job() {
  local id="$1"
  local reason="$2"
  DISABLED_COUNT=$((DISABLED_COUNT + 1))
  if $EXECUTE; then
    echo "  [$DISABLED_COUNT] Disabling $id — $reason"
    openclaw cron edit "$id" --disable
  else
    echo "  [$DISABLED_COUNT] Would disable $id — $reason"
  fi
}

# ============================================================
# S1: Duplicate name groups (18 jobs)
# ============================================================
echo "--- S1: Duplicate name groups (18 jobs) ---"
disable_job "e2dabeab-7b79-40a9-bd04-95de622b10eb" "錯誤記錄Hook dup"
disable_job "ff8e70dc-7f88-4891-90f8-1c5d28091f3a" "閉環-每日回顧 dup"
disable_job "19a8dc79-7c5f-4029-aa4f-3f7f2e2bc182" "SEO草稿生成 dup"
disable_job "5688dbca-8a03-4a91-88b7-b27e6080e239" "SEO草稿生成 dup"
disable_job "7bd183b6-2dc6-4fd5-8bde-5a785edf784d" "seo-draft dup"
disable_job "9dbf3bd4-482b-4741-bff7-711a040f0460" "gmail-summary dup"
disable_job "d640e239-4533-4ac5-bead-0e62e408a493" "Gmail摘要 dup"
disable_job "755952c0-f75a-45de-ac8a-eb9c0bb3e17d" "Gmail摘要 dup"
disable_job "92dd20e2-27f7-4a12-860b-d7b6e7d925d8" "stock-watch dup"
disable_job "4c6efe7c-b9a8-4e66-8c40-2952e1813385" "stock-watch dup"
disable_job "e6ff7b0b-da25-4fa6-8ad6-42cdf89bdb91" "social-plan dup"
disable_job "6bb58848-36ea-4ab2-a6c9-ee57e9173bcc" "社群發布建議 dup"
disable_job "d2d0984f-d8d5-4f90-a094-b7d9c3bc184d" "社群發布建議 dup"
disable_job "d0656f91-58e3-4d29-84f6-284e75463c1e" "YouTube分析 dup"
disable_job "c45cf99e-3943-47cc-9db0-233fdc7d8330" "SEO排名追蹤 dup"
disable_job "224817a7-ec79-4d28-86cd-a7b5de6344af" "美股觀察 dup"
disable_job "1df23d75-45e8-4ddb-b1d7-b1cc27f16186" "美股觀察 dup"
disable_job "492e0dc4-a717-40a2-94be-8d31f32d0c9a" "youtube-analytics dup"
echo ""

# ============================================================
# S2: AI閉環 vs 閉環 overlapping pairs (10 jobs)
# Keep 閉環 versions when both are ok; keep AI閉環 when 閉環 has errors
# ============================================================
echo "--- S2: AI閉環 vs 閉環 overlapping pairs (10 jobs) ---"
disable_job "68460461-4c6e-4e71-be72-34edc0749d77" "AI閉環-晨報 (keep 閉環-每日晨報)"
disable_job "bc1265e5-9b62-4155-abd4-4c4ef4340933" "AI閉環-YouTube (keep 閉環-YouTube分析)"
disable_job "4bdb9147-b0db-4e7a-8adf-0ccf1323f683" "AI閉環-競品 (keep 閉環-競品監控)"
disable_job "b553294b-0fff-4c6d-a829-e2f76a20ecc0" "閉環-SEO排名 (has error, keep AI閉環-SEO)"
disable_job "2d8b0ccd-2e33-43ed-a74f-dc1f26050dc7" "AI閉環-社群 (keep 閉環-社群建議)"
disable_job "7960f078-0f8b-4113-8591-4b0b8b6e3c82" "AI閉環-Gmail (keep 閉環-Gmail摘要)"
disable_job "aa32595c-e2f6-4fb3-ba0a-3ad881bab616" "閉環-美股觀察 (has error, keep AI閉環-美股)"
disable_job "ab8b113e-3413-44ee-988f-31d242befb96" "AI閉環-留言 (keep 閉環-留言分析)"
disable_job "14c01c86-f1b2-4e20-871c-224034cb2915" "AI閉環-靈感 (keep 閉環-靈感池)"
disable_job "583cc4e2-78eb-486d-b9d5-045292b0693d" "閉環-排程日誌 (has error, keep AI閉環-日誌)"
echo ""

# ============================================================
# S3: consecutiveErrors >= 3 (7 jobs)
# ============================================================
echo "--- S3: consecutiveErrors >= 3 (7 jobs) ---"
disable_job "5022e8cd-844f-408f-b109-90186bb573de" "照片生成提醒 ce=5"
disable_job "d7f6c124-6efc-4d8f-8e1d-90dea8ccf1c0" "測試-定期模擬任務 ce=3"
disable_job "1d4a9db9-8612-48e7-804b-30b1beef3bb2" "社群營銷-早晨研究 ce=3"
disable_job "1e4bdbba-1b30-4b17-8102-189653117294" "AI營銷-早晨研究 ce=3"
disable_job "3b7b44f1-400c-453d-ac55-b366ea34e552" "海膽社群發布 ce=4"
disable_job "f7fb685b-51f4-4709-b25c-827bda19ff14" "Skill-鈎子擴充 ce=4"
disable_job "de8987f9-4a86-4cde-8db7-95ea032e2532" "Skill-全面升級 ce=3"
echo ""

# ============================================================
# S4: Always-skip high-frequency (35 jobs)
# ============================================================
echo "--- S4: Always-skip high-frequency (35 jobs) ---"
disable_job "f9fb9c15-2542-453c-a0e1-8f4c56998559" "結合-Agent狀態鉤子 */15"
disable_job "50a3be40-d559-4d91-930e-76f8b8d83acf" "任務追蹤-狀態更新 */34"
disable_job "370c7669-4ecf-40b1-a8c0-167a65c42f67" "Agent中央調度 */33"
disable_job "469c9f97-a23b-4fb4-b0d6-6a868d776dc3" "閉環-學習優化 */38"
disable_job "2d41a041-32c8-4f7e-bbd5-23b1f6f9af1a" "Rhizome-數據標籤系統 */58"
disable_job "57bb8016-f5c7-4dc0-b2ef-489742a337af" "記憶體優化 */31"
disable_job "afe77c60-0842-47bf-9520-0656d48976cd" "向量庫即時更新 */30"
disable_job "0952edef-9584-4554-a272-8193ac984db6" "群組自主代理人 */53"
disable_job "c49a98dd-63e4-4d4a-a655-db8f3337cb04" "閉環-執行監控 */55"
disable_job "b099d842-69ee-486a-a339-f65fcd3e7ba5" "Session-對話存儲後清理 */52"
disable_job "e41ed607-8f37-4b22-a479-595675b94e24" "session-cleanup-rag */15"
disable_job "e220b61b-8712-4db9-b22e-273b7cfe355d" "向量索引-快速更新 */15"
disable_job "cddf4758-d853-4122-9493-feb644bcf499" "Kira-任務前向量查詢 */56"
disable_job "9fae3edc-b17b-4e53-9102-c91122885277" "continuous-sync */48"
disable_job "70c1db73-5976-41fe-8d67-f27bdd524b10" "RAG-Pipeline健康檢查 */29"
disable_job "fee189f1-d96e-4237-86c3-a89197d426d5" "Kira-Token使用監控 */15"
disable_job "49af1dcf-32ac-4d93-b464-1365b8899d7c" "hybrid-processing */59"
disable_job "a1fa5859-6404-49cc-bcd2-788720c4f127" "本地-預處理 */49"
disable_job "01a2a633-1e9b-49b9-a888-793766a63b5b" "混合模型路由 */35"
disable_job "2a9826dc-15fc-418e-aa71-c8d5b9bef9e2" "本地-對話摘要 */24"
disable_job "30d4dc28-4f41-497f-b865-e23336704ac2" "本地-學習記憶 */36"
disable_job "5fe3eac0-b281-4cf2-9603-8c958a3a0415" "Agent-領域識別 */42"
disable_job "9127b3e2-0af7-476e-adb3-bb8f23a3c044" "自動路由系統 */5"
disable_job "30ef5418-d1d1-4864-8169-dca3d4a65dd8" "向量庫-文檔掃描 */7"
disable_job "3fdd558b-49a7-4e4d-8921-5c2c6a3ce8dc" "向量庫-記憶整合 */37"
disable_job "b53c8353-7f01-4653-8d7b-634b4ad7c63d" "向量庫-實時更新 */41"
disable_job "70f643be-0550-40db-ba53-d0bd9c864082" "向量庫-批量處理 */43"
disable_job "b796bcb4-69d2-440d-8e37-0fca3c9594ab" "向量庫-質量提升 */47"
disable_job "95ec53de-a665-4883-8f13-9b2bf4a88569" "向量庫-關鍵詞強化 */53"
disable_job "68f9a8c5-378f-4ae2-9a24-0a28c17da01b" "向量庫-跨庫同步 */59"
disable_job "2b384959-1010-46fb-878c-0f79d3540357" "向量庫-系統日誌 */15"
disable_job "71e6fd1c-f9b1-4ff2-9702-21f46fdf6138" "向量庫-決策記錄 */17"
disable_job "60ea1a7b-992d-4c6d-9ad3-b55cb097b96c" "向量庫-用戶反饋 */19"
disable_job "c6d85dc6-c17e-494c-8f32-c9d6c43b05c6" "error-log-hook */15"
disable_job "9c0d6efa-7a35-4478-98ff-d347a602f6e2" "success-log-hook */15"
echo ""

# ============================================================
# S5: Redundant monitoring (5 jobs)
# ============================================================
echo "--- S5: Redundant monitoring (5 jobs) ---"
disable_job "1bc89ae9-a6e5-4126-b350-c217c58c52d9" "系統健康 (dup of sys-health-30m)"
disable_job "2a8dd7a6-8cfa-4efc-a073-36be30891510" "Security-安全監控 (dup of 安全監控)"
disable_job "f6913a95-43f3-4cb8-b45b-ca30ac21a4c5" "Heartbeat觸發記錄 */15 overhead"
disable_job "34bbcaee-acec-495f-89a8-994c9dedac05" "Heartbeat自動優化 daily-error"
disable_job "d25442ff-a57c-4094-8367-b75130f2501d" "Heartbeat穩定性監控 */20 overhead"
echo ""

# ============================================================
# Summary
# ============================================================
echo "==========================================="
echo "Total jobs to disable: $DISABLED_COUNT"
echo "==========================================="
if $EXECUTE; then
  echo "Done! All $DISABLED_COUNT jobs have been disabled."
  echo ""
  echo "To verify, run:"
  echo "  openclaw cron list | grep disabled"
else
  echo "This was a dry run. To actually disable these jobs, run:"
  echo "  ./cron_cleanup.sh --execute"
fi
