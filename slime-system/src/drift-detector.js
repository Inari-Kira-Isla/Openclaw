/**
 * DriftDetector - 漂移偵測器
 * 
 * 概念漂移、效能漂移、記憶衰減、行為漂移偵測
 * 閾值觸發與三級告警
 */

class DriftDetector {
  /**
   * @param {Object} baseline_metrics - 基準指標
   */
  constructor(baseline_metrics = {}) {
    // 預設基準線
    this.baseline = {
      accuracy: 0.85,
      p95_latency: 100, // ms
      recall: 0.80,
      output_distribution: null,
      ...baseline_metrics
    };

    // 滑動視窗大小
    this.window_size = 100;
    
    // 歷史指標記錄
    this.metrics_history = [];
    
    // 漂移閾值配置
    this.thresholds = {
      concept: {
        accuracy_drop: 0.15, // 下降 > 15%
        metric: 'accuracy'
      },
      performance: {
        latency_ratio: 2.0, // P95 > 基準線 2x
        metric: 'p95_latency'
      },
      memory_decay: {
        recall_drop: 0.20, // 下降 > 20%
        metric: 'recall'
      },
      behavior: {
        kl_divergence: 0.5, // KL-Divergence > 0.5
        metric: 'output_distribution'
      }
    };

    // 告警級別配置
    this.alert_levels = {
      LIGHT: 1,   // 輕度漂移 (1項超閾)
      MODERATE: 2, // 中度漂移 (2項超閾)
      SEVERE: 3   // 重度漂移 (3項超閾)
    };

    // 最後告警時間
    this.last_alert_time = null;
    this.alert_cooldown = 3600000; // 1小時冷卻
  }

  /**
   * 新增指標數據
   * @param {Object} metrics - 當前指標
   * @param {number} timestamp - 時間戳
   */
  addMetrics(metrics, timestamp = Date.now()) {
    const entry = { metrics, timestamp };
    this.metrics_history.push(entry);
    
    // 維持滑動視窗大小
    if (this.metrics_history.length > this.window_size) {
      this.metrics_history.shift();
    }
    
    return entry;
  }

  /**
   * 偵測漂移
   * @param {Object} current_metrics - 當前指標
   * @returns {Array} 漂移檢測結果陣列
   */
  detect(current_metrics) {
    const drifts = [];
    const timestamp = Date.now();

    // 1. 概念漂移偵測 - 預測準確率變化
    const acc_drift = this.baseline.accuracy - (current_metrics.accuracy || 0);
    if (acc_drift > this.thresholds.concept.accuracy_drop) {
      drifts.push({
        type: 'concept',
        severity: acc_drift,
        threshold: this.thresholds.concept.accuracy_drop,
        message: `概念漂移: 準確率下降 ${(acc_drift * 100).toFixed(1)}%`,
        baseline: this.baseline.accuracy,
        current: current_metrics.accuracy,
        timestamp
      });
    }

    // 2. 效能漂移偵測 - 響應時間
    const latency_ratio = (current_metrics.p95_latency || 0) / this.baseline.p95_latency;
    if (latency_ratio > this.thresholds.performance.latency_ratio) {
      drifts.push({
        type: 'performance',
        severity: latency_ratio,
        threshold: this.thresholds.performance.latency_ratio,
        message: `效能漂移: P95延遲為基準線 ${latency_ratio.toFixed(1)}x`,
        baseline: this.baseline.p95_latency,
        current: current_metrics.p95_latency,
        timestamp
      });
    }

    // 3. 記憶衰減偵測 - 召回率下降
    const recall_drop = this.baseline.recall - (current_metrics.recall || 0);
    if (recall_drop > this.thresholds.memory_decay.recall_drop) {
      drifts.push({
        type: 'memory_decay',
        severity: recall_drop,
        threshold: this.thresholds.memory_decay.recall_drop,
        message: `記憶衰減: 召回率下降 ${(recall_drop * 100).toFixed(1)}%`,
        baseline: this.baseline.recall,
        current: current_metrics.recall,
        timestamp
      });
    }

    // 4. 行為漂移偵測 - 輸出分佈變化 (KL-Divergence)
    if (current_metrics.output_distribution && this.baseline.output_distribution) {
      const kl_div = this._calculateKLDivergence(
        current_metrics.output_distribution,
        this.baseline.output_distribution
      );
      if (kl_div > this.thresholds.behavior.kl_divergence) {
        drifts.push({
          type: 'behavior',
          severity: kl_div,
          threshold: this.thresholds.behavior.kl_divergence,
          message: `行為漂移: KL-Divergence = ${kl_div.toFixed(3)}`,
          baseline: this.baseline.output_distribution,
          current: current_metrics.output_distribution,
          timestamp
        });
      }
    }

    // 記錄當前指標
    this.addMetrics(current_metrics, timestamp);

    return drifts;
  }

  /**
   * 計算 KL-Divergence
   * @param {Object} p - 當前分佈
   * @param {Object} q - 基準分佈
   * @returns {number} KL-Divergence 值
   */
  _calculateKLDivergence(p, q) {
    let kl_div = 0;
    const keys = new Set([...Object.keys(p || {}), ...Object.keys(q || {})]);
    
    for (const key of keys) {
      const p_val = p[key] || 0.0001;
      const q_val = q[key] || 0.0001;
      if (p_val > 0) {
        kl_div += p_val * Math.log(p_val / q_val);
      }
    }
    
    return Math.abs(kl_div);
  }

  /**
   * 計算告警級別
   * @param {Array} drifts - 漂移檢測結果
   * @returns {Object} 告警級別與建議
   */
  calculateAlertLevel(drifts) {
    const count = drifts.length;
    let level, action, color;

    if (count === 0) {
      level = 'NORMAL';
      action = '繼續監控';
      color = 'green';
    } else if (count === 1) {
      level = 'LIGHT';
      action = '記錄日誌，增加監控頻率';
      color = 'yellow';
    } else if (count === 2) {
      level = 'MODERATE';
      action = '觸發增量學習';
      color = 'orange';
    } else {
      level = 'SEVERE';
      action = '觸發完整重訓練';
      color = 'red';
    }

    return {
      level,
      level_code: this.alert_levels[level] || 0,
      action,
      color,
      drift_count: count,
      drifts
    };
  }

  /**
   * 計算漂移分數 (0-1)
   * @param {Array} drifts - 漂移檢測結果
   * @returns {number} 漂移分數
   */
  calculateDriftScore(drifts) {
    if (drifts.length === 0) return 0;
    
    // 根據嚴重程度和數量計算分數
    const severity_sum = drifts.reduce((sum, d) => sum + Math.min(d.severity, 1), 0);
    const count_factor = Math.min(drifts.length / 4, 1); // 最多4項
    const avg_severity = severity_sum / drifts.length;
    
    return Math.min((avg_severity * 0.7 + count_factor * 0.3), 1);
  }

  /**
   * 檢查是否應該觸發告警
   * @param {Array} drifts - 漂移檢測結果
   * @returns {boolean}
   */
  shouldAlert(drifts) {
    if (drifts.length === 0) return false;
    
    const now = Date.now();
    if (this.last_alert_time && (now - this.last_alert_time) < this.alert_cooldown) {
      return false;
    }
    
    this.last_alert_time = now;
    return true;
  }

  /**
   * 更新基準線
   * @param {Object} new_metrics - 新基準指標
   */
  update_baseline(new_metrics) {
    const updated = { ...this.baseline };
    
    if (new_metrics.accuracy !== undefined) {
      updated.accuracy = new_metrics.accuracy;
    }
    if (new_metrics.p95_latency !== undefined) {
      updated.p95_latency = new_metrics.p95_latency;
    }
    if (new_metrics.recall !== undefined) {
      updated.recall = new_metrics.recall;
    }
    if (new_metrics.output_distribution !== undefined) {
      updated.output_distribution = new_metrics.output_distribution;
    }
    
    this.baseline = updated;
    console.log(`[DriftDetector] 基準線已更新:`, this.baseline);
  }

  /**
   * 獲取歷史漂移記錄
   * @param {number} limit - 返回數量限制
   * @returns {Array}
   */
  getHistory(limit = 10) {
    return this.metrics_history.slice(-limit);
  }

  /**
   * 獲取當前狀態摘要
   * @returns {Object}
   */
  getStatus() {
    const recent = this.metrics_history.slice(-10);
    const latest = recent[recent.length - 1];
    
    return {
      baseline: this.baseline,
      window_size: this.window_size,
      history_count: this.metrics_history.length,
      last_update: latest?.timestamp || null,
      thresholds: this.thresholds
    };
  }
}

/**
 * 建立工廠函數
 * @param {Object} config - 配置
 * @returns {DriftDetector}
 */
function createDriftDetector(config = {}) {
  return new DriftDetector(config.baseline_metrics);
}

module.exports = {
  DriftDetector,
  createDriftDetector
};
