---
name: load_balancer
description: 負載平衡。當需要分配系統資源和任務負載時觸發，包括：負載計算、分配策略、健康檢查、故障轉移。
---

# Load Balancer

## 負載評估

### 指標
- CPU 使用率
- 記憶體使用
- 請求排隊
- 回應時間

## 分配策略

### Round Robin
輪流分配給每個節點

### Least Connections
分配給連線數最少的

### Weighted
根據能力加權分配

### 故障轉移
偵測到節點故障時，自動轉移到健康節點
