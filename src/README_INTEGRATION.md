# Lazy Uni Shop - System Integration

## 系統整合總覽

本專案整合了三大核心系統：
1. 🎨 動畫系統（Spine 2D）
2. 🎨 主題系統（深色/淺色）
3. 📡 數據層對接

---

## 1. 動畫系統 🎬

**位置：** `src/animations/spineAnimation.ts`

### 狀態機

| 狀態 | 說明 |
|------|------|
| idle | 待機 |
| work_typing | 打字中 |
| work_writing | 寫作中 |
| work_browsing | 瀏覽中 |
| idle_thinking | 思考中 |
| communication_talk | 對話中 |
| stress_warning | 壓力警告 |
| special_celebrate | 慶祝 |

### 觸發事件

```typescript
animationManager.trigger('bob', 'onTaskAssigned');
animationManager.trigger('bob', 'onLLMReasoning');
animationManager.trigger('bob', 'onTokenLimitWarning');
```

---

## 2. 主題系統 🎨

**位置：** `src/theme/colors.ts`

### 使用方式

```typescript
import { darkTheme, lightTheme } from './theme/colors';

// 深色主題
const dark = darkTheme;

// 淺色主題  
const light = lightTheme;

// CSS 變數
document.documentElement.style.setProperty('--background', dark.background);
```

### 主題切換

```typescript
function toggleTheme() {
  const isDark = document.body.classList.contains('dark');
  document.body.classList.toggle('dark', !isDark);
  document.body.classList.toggle('light', isDark);
}
```

---

## 3. 數據層 📡

**位置：** `src/data/agentData.ts`

### 數據結構

```typescript
interface Agent {
  id: string;
  name: string;
  role: string;
  avatar: string;
  color: string;
  status: 'online' | 'busy' | 'thinking' | 'offline';
  currentTask: string;
  progress: number;
}
```

### API 接口

```typescript
import api from './data/agentData';

// 獲取所有 Agent
const agents = await api.getAgents();

// 獲取事件
const events = await api.getEvents();

// 即時訂閱
const unsubscribe = api.subscribe((data) => {
  console.log('數據更新:', data);
});
```

---

## 整合示例

```typescript
import { AnimationManager, getAnimationState } from './animations/spineAnimation';
import { darkTheme, lightTheme } from './theme/colors';
import api, { Agent } from './data/agentData';

class LazyUniShopApp {
  private animationManager = new AnimationManager();
  private currentTheme = darkTheme;
  
  async init() {
    // 載入數據
    const data = await api.getDashboardData();
    
    // 初始化動畫狀態
    data.agents.forEach((agent: Agent) => {
      const state = getAnimationState(agent.status);
      this.animationManager.setState(agent.id, state);
    });
    
    // 訂閱更新
    api.subscribe((newData) => {
      this.handleUpdate(newData);
    });
  }
  
  private handleUpdate(data: any) {
    // 更新 UI
    // 觸发动画
  }
  
  setTheme(theme: 'dark' | 'light') {
    this.currentTheme = theme === 'dark' ? darkTheme : lightTheme;
    // 應用主題
  }
}
```

---

## 文件結構

```
src/
├── animations/
│   └── spineAnimation.ts    # 動畫系統
├── theme/
│   └── colors.ts            # 主題系統
├── data/
│   └── agentData.ts         # 數據層
└── App.tsx                  # 主應用
```

---

## 下一步

- [ ] 整合 React 組件
- [ ] 添加 WebSocket 即時更新
- [ ] 添加更多動畫狀態
- [ ] 優化主題過渡效果
