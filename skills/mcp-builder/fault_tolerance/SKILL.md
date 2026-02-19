---
name: fault_tolerance
description: 容錯與錯誤處理。當需要為系統添加錯誤處理和容錯機制時觸發，包括：重試策略、降級處理、超時控制、熔斷機制。
---

# Fault Tolerance

## 重試策略

### 指數退避
```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: { maxRetries: number; baseDelay: number }
): Promise<T> {
  for (let i = 0; i < options.maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === options.maxRetries - 1) throw error;
      await sleep(options.baseDelay * Math.pow(2, i));
    }
  }
  throw new Error('Max retries exceeded');
}
```

### 重試配置
```json
{
  "max_retries": 3,
  "base_delay": 1000,
  "max_delay": 30000,
  "backoff": "exponential",
  "retry_on": ["timeout", "network_error"]
}
```

## 降級處理

### 降級策略
| 層級 | 策略 |
|------|------|
| L1 | 緩存回退 |
| L2 | 預設值回退 |
| L3 | 降級服務 |
| L4 | 優雅失敗 |

### 實現模式
```typescript
async function withFallback<T>(
  primary: () => Promise<T>,
  fallback: () => Promise<T>
): Promise<T> {
  try {
    return await primary();
  } catch (error) {
    return await fallback();
  }
}
```

## 超時控制

```typescript
async function withTimeout<T>(
  fn: () => Promise<T>,
  timeoutMs: number
): Promise<T> {
  return Promise.race([
    fn(),
    new Promise<T>((_, reject) => 
      setTimeout(() => reject(new Error('Timeout')), timeoutMs)
    )
  ]);
}
```

## 熔斷機制

```
狀態：closed → open → half-open

closed: 正常運作，記錄失敗次數
open: 快速失敗，不執行請求
half-open: 測試服務是否恢復
```

```typescript
class CircuitBreaker {
  private failures = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      throw new Error('Circuit open');
    }
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
}
```
