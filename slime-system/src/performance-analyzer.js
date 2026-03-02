/**
 * PerformanceAnalyzer - 效能分析器
 * 
 * 四維度指標：學習效率、記憶效率、泛化能力、資源消耗
 * 異常檢測與根因分析
 */

class PerformanceAnalyzer {
  constructor(config = {}) {
    // 配置參數
    this.config = {
      anomaly_threshold: 2.0, // 標準差倍數
      trend_window: 10,       // 趨勢分析視窗
      min_samples: 5,         // 最小樣本數
      ...config
    };

    // 四維度指標收集
    this.dimensions = {
      learning_efficiency: {  // 學習效率
        metrics: ['epoch_time', 'loss_reduction', 'sample_efficiency'],
        weights: { epoch_time: 0.3, loss_reduction: 0.4, sample_efficiency: 0.3 }
      },
      memory_efficiency: {    // 記憶效率
        metrics: ['memory_usage', 'access_latency', 'retention_rate'],
        weights: { memory_usage: 0.4, access_latency: 0.3, retention_rate: 0.3 }
      },
      generalization: {       // 泛化能力
        metrics: ['validation_accuracy', 'transfer_score', 'robustness'],
        weights: { validation_accuracy: 0.5, transfer_score: 0.3, robustness: 0.2 }
      },
      resource_consumption: { // 資源消耗
        metrics: ['cpu_usage', 'gpu_usage', 'io_wait'],
        weights: { cpu_usage: 0.4, gpu_usage: 0.3, io_wait: 0.3 }
      }
    };

    // 歷史數據
    this.history = {
      learning_efficiency: [],
      memory_efficiency: [],
      generalization: [],
      resource_consumption: [],
      raw_metrics: []
    };

    // 健康度閾值
    this.health_thresholds = {
      excellent: 85,
      good: 70,
      fair: 50,
      poor: 30
    };
  }

  /**
   * 添加指標數據
   * @param {Object} metrics - 原始指標數據
   */
  addMetrics(metrics) {
    const timestamp = Date.now();
    
    // 解析並分類指標
    const parsed = this._parseMetrics(metrics);
    
    // 存儲原始數據
    this.history.raw_metrics.push({ ...metrics, timestamp });
    
    // 存儲各維度數據
    for (const [dimension, data] of Object.entries(parsed)) {
      if (this.history[dimension]) {
        this.history[dimension].push({ ...data, timestamp });
      }
    }

    // 維持歷史大小限制
    const max_history = this.config.trend_window * 10;
    for (const key of Object.keys(this.history)) {
      if (this.history[key].length > max_history) {
        this.history[key] = this.history[key].slice(-max_history);
      }
    }
  }

  /**
   * 解析原始指標
   * @param {Object} metrics - 原始指標
   * @returns {Object} 解析後的維度數據
   */
  _parseMetrics(metrics) {
    return {
      learning_efficiency: {
        epoch_time: metrics.epoch_time || 0,
        loss_reduction: metrics.loss_reduction || 0,
        sample_efficiency: metrics.sample_efficiency || 0
      },
      memory_efficiency: {
        memory_usage: metrics.memory_usage || 0,
        access_latency: metrics.access_latency || 0,
        retention_rate: metrics.retention_rate || 0
      },
      generalization: {
        validation_accuracy: metrics.validation_accuracy || 0,
        transfer_score: metrics.transfer_score || 0,
        robustness: metrics.robustness || 0
      },
      resource_consumption: {
        cpu_usage: metrics.cpu_usage || 0,
        gpu_usage: metrics.gpu_usage || 0,
        io_wait: metrics.io_wait || 0
      }
    };
  }

  /**
   * 執行完整分析
   * @returns {Object} 分析報告
   */
  analyze() {
    const report = {
      timestamp: Date.now(),
      summary: {},
      trends: {},
      anomalies: [],
      bottlenecks: [],
      recommendations: [],
      health_score: 0,
      health_status: 'unknown'
    };

    // 1. 趨勢分析
    report.trends = this._analyzeTrends();
    
    // 2. 異常檢測
    report.anomalies = this._detectAnomalies();
    
    // 3. 瓶頸識別
    report.bottlenecks = this._identifyBottlenecks();
    
    // 4. 生成摘要
    report.summary = this._generateSummary(report.trends, report.bottlenecks);
    
    // 5. 生成建議
    report.recommendations = this._generateRecommendations(
      report.summary,
      report.bottlenecks,
      report.anomalies
    );
    
    // 6. 計算健康度
    const health = this._calculateHealthScore(report);
    report.health_score = health.score;
    report.health_status = health.status;

    return report;
  }

  /**
   * 趨勢分析
   * @returns {Object}
   */
  _analyzeTrends() {
    const trends = {};
    const window = this.config.trend_window;

    for (const [dimension, data] of Object.entries(this.history)) {
      if (dimension === 'raw_metrics' || data.length < 2) continue;
      
      const recent = data.slice(-window);
      if (recent.length < 2) continue;

      const metrics = {};
      const metric_keys = Object.keys(recent[0]).filter(k => k !== 'timestamp');
      
      for (const key of metric_keys) {
        const values = recent.map(r => r[key]).filter(v => typeof v === 'number');
        if (values.length < 2) continue;
        
        // 計算移動平均
        const ma = values.reduce((a, b) => a + b, 0) / values.length;
        
        // 計算趨勢斜率 (線性迴歸)
        const n = values.length;
        const x_mean = (n - 1) / 2;
        const y_mean = ma;
        
        let numerator = 0, denominator = 0;
        for (let i = 0; i < n; i++) {
          numerator += (i - x_mean) * (values[i] - y_mean);
          denominator += Math.pow(i - x_mean, 2);
        }
        
        const slope = denominator !== 0 ? numerator / denominator : 0;
        const normalized_slope = ma !== 0 ? slope / ma : 0; // 標準化斜率
        
        // 判斷趨勢方向
        let direction;
        if (Math.abs(normalized_slope) < 0.02) {
          direction = 'stable';
        } else if (normalized_slope > 0) {
          direction = key.includes('usage') || key.includes('time') || key.includes('latency') 
            ? 'worsening' : 'improving';
        } else {
          direction = key.includes('usage') || key.includes('time') || key.includes('latency')
            ? 'improving' : 'worsening';
        }
        
        metrics[key] = {
          moving_average: ma,
          slope: normalized_slope,
          direction,
          sample_count: values.length
        };
      }
      
      trends[dimension] = metrics;
    }

    return trends;
  }

  /**
   * 異常檢測
   * @returns {Array}
   */
  _detectAnomalies() {
    const anomalies = [];
    const window = this.config.trend_window;
    const threshold = this.config.anomaly_threshold;

    for (const [dimension, data] of Object.entries(this.history)) {
      if (dimension === 'raw_metrics' || data.length < this.config.min_samples) continue;
      
      const recent = data.slice(-window);
      const metric_keys = Object.keys(recent[0]).filter(k => k !== 'timestamp');
      
      for (const key of metric_keys) {
        const values = recent.map(r => r[key]).filter(v => typeof v === 'number');
        if (values.length < this.config.min_samples) continue;
        
        // 計算均值和標準差
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const variance = values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / values.length;
        const std = Math.sqrt(variance);
        
        // 檢查最新值是否異常
        const latest_value = values[values.length - 1];
        if (std > 0) {
          const z_score = Math.abs((latest_value - mean) / std);
          
          if (z_score > threshold) {
            anomalies.push({
              dimension,
              metric: key,
              value: latest_value,
              expected_range: [mean - std * threshold, mean + std * threshold],
              z_score,
              severity: z_score > threshold * 2 ? 'high' : 'medium',
              timestamp: recent[recent.length - 1].timestamp
            });
          }
        }
      }
    }

    return anomalies;
  }

  /**
   * 識別瓶頸
   * @returns {Array}
   */
  _identifyBottlenecks() {
    const bottlenecks = [];
    
    // 檢查各維度的趨勢
    const trends = this._analyzeTrends();
    
    // 記憶體使用率過高
    if (trends.memory_efficiency?.memory_usage) {
      const mem = trends.memory_efficiency.memory_usage;
      if (mem.moving_average > 85 || mem.direction === 'worsening') {
        bottlenecks.push({
          type: 'memory',
          severity: mem.moving_average > 90 ? 'high' : 'medium',
          metric: 'memory_usage',
          value: mem.moving_average,
          description: `記憶體使用率 ${mem.moving_average.toFixed(1)}% - ${mem.direction === 'worsening' ? '持續上升' : '過高'}`
        });
      }
    }

    // I/O 延遲增加
    if (trends.memory_efficiency?.access_latency) {
      const io = trends.memory_efficiency.access_latency;
      if (io.direction === 'worsening') {
        bottlenecks.push({
          type: 'io',
          severity: 'medium',
          metric: 'access_latency',
          value: io.moving_average,
          description: `I/O 延遲增加，趨勢: ${io.direction}`
        });
      }
    }

    // CPU/GPU 資源緊張
    if (trends.resource_consumption?.cpu_usage || trends.resource_consumption?.gpu_usage) {
      const cpu = trends.resource_consumption.cpu_usage;
      const gpu = trends.resource_consumption.gpu_usage;
      
      if (cpu && cpu.moving_average > 80) {
        bottlenecks.push({
          type: 'compute',
          severity: cpu.moving_average > 90 ? 'high' : 'medium',
          metric: 'cpu_usage',
          value: cpu.moving_average,
          description: `CPU 使用率過高: ${cpu.moving_average.toFixed(1)}%`
        });
      }
      
      if (gpu && gpu.moving_average > 80) {
        bottlenecks.push({
          type: 'compute',
          severity: gpu.moving_average > 90 ? 'high' : 'medium',
          metric: 'gpu_usage',
          value: gpu.moving_average,
          description: `GPU 使用率過高: ${gpu.moving_average.toFixed(1)}%`
        });
      }
    }

    // 泛化能力下降
    if (trends.generalization?.validation_accuracy) {
      const acc = trends.generalization.validation_accuracy;
      if (acc.direction === 'worsening') {
        bottlenecks.push({
          type: 'generalization',
          severity: 'high',
          metric: 'validation_accuracy',
          value: acc.moving_average,
          description: `驗證集準確率下降: ${acc.direction}`
        });
      }
    }

    return bottlenecks;
  }

  /**
   * 生成摘要
   * @param {Object} trends - 趨勢數據
   * @param {Array} bottlenecks - 瓶頸列表
   * @returns {Object}
   */
  _generateSummary(trends, bottlenecks) {
    let overall_trend = 'stable';
    let improving_count = 0;
    let worsening_count = 0;
    
    // 統計趨勢方向
    for (const dimension of Object.values(trends)) {
      for (const metric of Object.values(dimension)) {
        if (metric.direction === 'improving') improving_count++;
        if (metric.direction === 'worsening') worsening_count++;
      }
    }
    
    if (worsening_count > improving_count) {
      overall_trend = 'declining';
    } else if (improving_count > worsening_count) {
      overall_trend = 'improving';
    }
    
    // 計算趨勢表情符號
    const trend_emoji = {
      improving: '📈',
      declining: '📉',
      stable: '➡️'
    };

    return {
      overall_trend,
      trend_emoji: trend_emoji[overall_trend],
      improving_count,
      worsening_count,
      bottleneck_count: bottlenecks.length,
      dimensions_analyzed: Object.keys(trends).length
    };
  }

  /**
   * 生成建議
   * @param {Object} summary - 摘要
   * @param {Array} bottlenecks - 瓶頸
   * @param {Array} anomalies - 異常
   * @returns {Array}
   */
  _generateRecommendations(summary, bottlenecks, anomalies) {
    const recommendations = [];

    // 基於瓶頸生成建議
    for (const bottleneck of bottlenecks) {
      switch (bottleneck.type) {
        case 'memory':
          recommendations.push({
            priority: bottleneck.severity === 'high' ? '高' : '中',
            category: '記憶體優化',
            action: '增加記憶體緩衝區大小',
            reason: bottleneck.description
          });
          recommendations.push({
            priority: '中',
            category: '記憶體優化',
            action: '優化記憶體回收策略',
            reason: '減少記憶碎片'
          });
          break;
          
        case 'io':
          recommendations.push({
            priority: '中',
            category: 'I/O 優化',
            action: '優化 I/O 批次處理',
            reason: bottleneck.description
          });
          break;
          
        case 'compute':
          recommendations.push({
            priority: bottleneck.severity === 'high' ? '高' : '中',
            category: '計算資源',
            action: '擴展計算資源或優化並行度',
            reason: bottleneck.description
          });
          break;
          
        case 'generalization':
          recommendations.push({
            priority: '高',
            category: '模型優化',
            action: '增加正則化或資料增強',
            reason: '泛化能力下降，需防止過擬合'
          });
          break;
      }
    }

    // 基於異常生成建議
    for (const anomaly of anomalies) {
      if (anomaly.severity === 'high') {
        recommendations.push({
          priority: '高',
          category: '異常處理',
          action: `檢查 ${anomaly.metric} 異常`,
          reason: `檢測到 ${anomaly.dimension}.${anomaly.metric} 異常偏離 (z=${anomaly.z_score.toFixed(2)})`
        });
      }
    }

    // 如果沒有問題，添加積極建議
    if (recommendations.length === 0) {
      recommendations.push({
        priority: '低',
        category: '持續優化',
        action: '系統運行良好，可考慮進一步優化',
        reason: '各項指標正常'
      });
    }

    // 按優先級排序
    const priority_order = { '高': 0, '中': 1, '低': 2 };
    recommendations.sort((a, b) => priority_order[a.priority] - priority_order[b.priority]);

    return recommendations;
  }

  /**
   * 計算健康度分數
   * @param {Object} report - 分析報告
   * @returns {Object}
   */
  _calculateHealthScore(report) {
    let score = 100;
    
    // 扣分項
    const penalties = [
      { condition: report.summary.bottleneck_count >= 3, deduct: 30 },
      { condition: report.summary.bottleneck_count >= 1, deduct: 15 },
      { condition: report.anomalies.filter(a => a.severity === 'high').length > 0, deduct: 20 },
      { condition: report.anomalies.length > 0, deduct: 10 },
      { condition: report.summary.overall_trend === 'declining', deduct: 25 },
    ];
    
    for (const penalty of penalties) {
      if (penalty.condition) {
        score -= penalty.deduct;
      }
    }
    
    score = Math.max(0, Math.min(100, score));
    
    // 判斷狀態
    let status;
    if (score >= this.health_thresholds.excellent) {
      status = 'excellent';
    } else if (score >= this.health_thresholds.good) {
      status = 'good';
    } else if (score >= this.health_thresholds.fair) {
      status = 'fair';
    } else {
      status = 'poor';
    }
    
    return { score, status };
  }

  /**
   * 生成 Markdown 格式報告
   * @returns {string}
   */
  generateMarkdownReport() {
    const report = this.analyze();
    
    let md = `## 效能分析報告\n\n`;
    md += `### 摘要\n`;
    md += `- 整體健康度: ${report.health_score}/100\n`;
    md += `- 趨勢: ${report.summary.trend_emoji} ${report.summary.overall_trend}\n`;
    md += `- 改善項目: ${report.summary.improving_count}\n`;
    md += `- 惡化項目: ${report.summary.worsening_count}\n\n`;
    
    md += `### 瓶頸\n`;
    if (report.bottlenecks.length === 0) {
      md += `- 無明顯瓶頸\n`;
    } else {
      for (const b of report.bottlenecks) {
        md += `- ${b.description} - ${b.severity}\n`;
      }
    }
    md += `\n`;
    
    md += `### 異常\n`;
    if (report.anomalies.length === 0) {
      md += `- 無異常檢測\n`;
    } else {
      for (const a of report.anomalies) {
        md += `- ${a.dimension}.${a.metric}: ${a.severity}\n`;
      }
    }
    md += `\n`;
    
    md += `### 建議\n`;
    for (const r of report.recommendations) {
      md += `- [${r.priority}] ${r.action}\n`;
    }
    
    return md;
  }

  /**
   * 獲取狀態
   * @returns {Object}
   */
  getStatus() {
    return {
      dimensions: Object.keys(this.dimensions),
      history_sizes: Object.fromEntries(
        Object.entries(this.history).map(([k, v]) => [k, v.length])
      ),
      config: this.config
    };
  }
}

/**
 * 建立工廠函數
 * @param {Object} config - 配置
 * @returns {PerformanceAnalyzer}
 */
function createPerformanceAnalyzer(config = {}) {
  return new PerformanceAnalyzer(config);
}

module.exports = {
  PerformanceAnalyzer,
  createPerformanceAnalyzer
};
