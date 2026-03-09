/**
 * Reward Function 計算器
 * 輸入維度：success_rate, speed, user_satisfaction, error_count
 * 輸出：-1 到 1 既 reward score
 */

function calculateReward(params) {
  const { success = true, speedMs = 0, userRating = 0, errorCount = 0 } = params;
  
  let score = 0;
  
  // 基礎分數：成功與否
  if (success) {
    score += 0.4;
  } else {
    score -= 0.5;
  }
  
  // 速度獎勵（越快越好）
  if (speedMs > 0) {
    if (speedMs < 1000) score += 0.2;      // < 1s
    else if (speedMs < 5000) score += 0.1;  // < 5s
    else if (speedMs > 30000) score -= 0.1; // > 30s
  }
  
  // 用戶評分（-1 到 1）
  score += userRating * 0.3;
  
  // 錯誤懲罰
  score -= errorCount * 0.15;
  
  // 限制範圍 [-1, 1]
  score = Math.max(-1, Math.min(1, score));
  
  return {
    score: Math.round(score * 100) / 100,
    breakdown: { success, speedMs, userRating, errorCount }
  };
}

// CLI
const args = process.argv.slice(2);
if (args[0]) {
  const params = {
    success: args[0] === 'true',
    speedMs: parseInt(args[1]) || 0,
    userRating: parseFloat(args[2]) || 0,
    errorCount: parseInt(args[3]) || 0
  };
  const result = calculateReward(params);
  console.log('📊 Reward Score:', result.score);
  console.log('   Breakdown:', result.breakdown);
} else {
  console.log('用法: node reward.js <success> [speedMs] [userRating] [errorCount]');
  console.log('例: node reward.js true 1500 0.5 0');
}
