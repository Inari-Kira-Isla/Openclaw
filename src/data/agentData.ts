// ============================================
// Lazy Uni Shop - Data Layer
// 數據層對接
// ============================================

export interface Agent {
  id: string;
  name: string;
  role: string;
  avatar: string;
  color: string;
  status: 'online' | 'busy' | 'thinking' | 'offline';
  currentTask: string;
  progress: number;
  lastUpdate: number;
}

export interface Event {
  id: string;
  type: 'warning' | 'error' | 'success' | 'info';
  agentId: string;
  title: string;
  description: string;
  timestamp: number;
}

export interface Activity {
  id: string;
  agentId: string;
  action: string;
  timestamp: number;
}

export interface DashboardData {
  agents: Agent[];
  events: Event[];
  activities: Activity[];
  stats: {
    onlineCount: number;
    busyCount: number;
    totalTasks: number;
    pendingEvents: number;
  };
}

// 模擬數據
export const mockAgents: Agent[] = [
  {
    id: 'georgia',
    name: 'Georgia',
    role: '遊戲顧問',
    avatar: '🎮',
    color: 'purple',
    status: 'online',
    currentTask: '正在回覆客戶問題',
    progress: 75,
    lastUpdate: Date.now(),
  },
  {
    id: 'alice',
    name: 'Alice',
    role: '寫作大師',
    avatar: '📝',
    color: 'pink',
    status: 'busy',
    currentTask: '撰寫每週報告',
    progress: 45,
    lastUpdate: Date.now(),
  },
  {
    id: 'bob',
    name: 'Bob',
    role: 'IT 工程師',
    avatar: '💻',
    color: 'cyan',
    status: 'thinking',
    currentTask: 'Debug 系統錯誤',
    progress: 90,
    lastUpdate: Date.now(),
  },
  {
    id: 'carol',
    name: 'Carol',
    role: '數據分析師',
    avatar: '🔬',
    color: 'green',
    status: 'online',
    currentTask: '分析市場趨勢',
    progress: 60,
    lastUpdate: Date.now(),
  },
  {
    id: 'dave',
    name: 'Dave',
    role: '科技偵察',
    avatar: '🔧',
    color: 'orange',
    status: 'offline',
    currentTask: '等待任務分配',
    progress: 0,
    lastUpdate: Date.now(),
  },
  {
    id: 'eva',
    name: 'Eva',
    role: '分析師',
    avatar: '📊',
    color: 'red',
    status: 'online',
    currentTask: '監控 RSS feeds',
    progress: 100,
    lastUpdate: Date.now(),
  },
];

export const mockEvents: Event[] = [
  {
    id: 'evt_001',
    type: 'warning',
    agentId: 'bob',
    title: 'Bob 需要幫忙！',
    description: 'API 連接失敗，需要用戶確認',
    timestamp: Date.now(),
  },
];

export const mockActivities: Activity[] = [
  { id: 'act_001', agentId: 'georgia', action: '完成對話 #15', timestamp: Date.now() - 60000 },
  { id: 'act_002', agentId: 'alice', action: '提交報告草稿', timestamp: Date.now() - 120000 },
  { id: 'act_003', agentId: 'carol', action: '生成分析報告', timestamp: Date.now() - 180000 },
];

// 計算統計數據
export function calculateStats(agents: Agent[]): DashboardData['stats'] {
  return {
    onlineCount: agents.filter(a => a.status === 'online').length,
    busyCount: agents.filter(a => a.status === 'busy' || a.status === 'thinking').length,
    totalTasks: agents.filter(a => a.progress > 0).length,
    pendingEvents: mockEvents.length,
  };
}

// 獲取完整數據
export function getDashboardData(): DashboardData {
  return {
    agents: mockAgents,
    events: mockEvents,
    activities: mockActivities,
    stats: calculateStats(mockAgents),
  };
}

// API 接口（可對接 OpenClaw）
export const api = {
  getAgents: () => Promise.resolve(mockAgents),
  getEvents: () => Promise.resolve(mockEvents),
  getActivities: () => Promise.resolve(mockActivities),
  getDashboard: () => Promise.resolve(getDashboardData()),
  
  // WebSocket 模擬
  subscribe: (callback: (data: DashboardData) => void) => {
    const interval = setInterval(() => {
      callback(getDashboardData());
    }, 5000);
    return () => clearInterval(interval);
  },
};

export default api;
