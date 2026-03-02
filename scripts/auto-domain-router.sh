#!/bin/bash
# Auto Domain Router Script v2

echo "=== Auto Domain Router ==="

# 接收任務
TASK="$1"

# 識別領域 (增強中文匹配)
if echo "$TASK" | grep -qiE "code|程式|開發|debug|寫程式|coding"; then
    AGENT="code-master"
    DOMAIN="coding"
elif echo "$TASK" | grep -qiE "文案|寫作|文章|內容|文字|copy|文章"; then
    AGENT="writing-master"
    DOMAIN="writing"
elif echo "$TASK" | grep -qiE "設計|UI|UX|圖形|介面|視覺"; then
    AGENT="design-master"
    DOMAIN="design"
elif echo "$TASK" | grep -qiE "分析|數據|統計|圖表|report"; then
    AGENT="analytics-agent"
    DOMAIN="analysis"
elif echo "$TASK" | grep -qiE "記憶|向量|rag|檢索|搜索"; then
    AGENT="memory-agent"
    DOMAIN="memory"
elif echo "$TASK" | grep -qiE "治理|決策|政策|規則"; then
    AGENT="governance-agent"
    DOMAIN="governance"
elif echo "$TASK" | grep -qiE "審查|裁決|評估|判斷|審核"; then
    AGENT="neicheok"
    DOMAIN="review"
elif echo "$TASK" | grep -qiE "質疑|挑戰|改進|優化|建議"; then
    AGENT="evolution"
    DOMAIN="evolution"
elif echo "$TASK" | grep -qiE "執行|任務|行動|完成|做"; then
    AGENT="team"
    DOMAIN="execution"
elif echo "$TASK" | grep -qiE "學習|訓練|成長|教育"; then
    AGENT="slime"
    DOMAIN="learning"
elif echo "$TASK" | grep -qiE "創意|策略|策劃|靈感|idea"; then
    AGENT="muse-core"
    DOMAIN="creative"
else
    AGENT="main"
    DOMAIN="default"
fi

echo "Task: $TASK"
echo "Domain: $DOMAIN"
echo "Agent: $AGENT"

echo ""
echo "=== 路由完成 ==="
