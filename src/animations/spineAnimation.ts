// ============================================
// Lazy Uni Shop - Animation System
// 動畫系統 - Spine 2D 狀態機整合
// ============================================

export type AnimationState = 
  | 'idle' 
  | 'idle_normal' 
  | 'idle_thinking'
  | 'work' 
  | 'work_typing'
  | 'work_writing'
  | 'work_browsing'
  | 'communication'
  | 'communication_talk'
  | 'communication_listen'
  | 'movement'
  | 'movement_walk'
  | 'stress'
  | 'stress_warning'
  | 'special'
  | 'special_celebrate';

export interface AnimationTransition {
  from: AnimationState | 'any';
  to: AnimationState;
  trigger: string;
  duration: number; // ms
}

export interface AgentAnimationConfig {
  agentId: string;
  defaultState: AnimationState;
  states: Record<AnimationState, {
    loop: boolean;
    duration?: number;
    speed: number;
  }>;
}

// 動畫狀態配置
export const animationConfigs: Record<string, AgentAnimationConfig> = {
  georgia: {
    agentId: 'georgia',
    defaultState: 'work_typing',
    states: {
      idle: { loop: true, speed: 1 },
      idle_normal: { loop: true, speed: 1 },
      idle_thinking: { loop: true, speed: 1 },
      work: { loop: true, speed: 1 },
      work_typing: { loop: true, speed: 1.5 },
      work_writing: { loop: true, speed: 1.2 },
      work_browsing: { loop: true, speed: 1 },
      communication: { loop: false, duration: 2000, speed: 1 },
      communication_talk: { loop: false, duration: 1500, speed: 1 },
      communication_listen: { loop: true, speed: 1 },
      movement: { loop: false, duration: 1000, speed: 1 },
      movement_walk: { loop: true, speed: 1 },
      stress: { loop: true, speed: 1.5 },
      stress_warning: { loop: true, speed: 2 },
      special: { loop: false, duration: 3000, speed: 1 },
      special_celebrate: { loop: false, duration: 2000, speed: 1.5 },
    },
  },
  alice: {
    agentId: 'alice',
    defaultState: 'work_writing',
    states: {
      idle: { loop: true, speed: 1 },
      idle_normal: { loop: true, speed: 1 },
      idle_thinking: { loop: true, speed: 1 },
      work: { loop: true, speed: 1 },
      work_typing: { loop: true, speed: 1.2 },
      work_writing: { loop: true, speed: 1.5 },
      work_browsing: { loop: true, speed: 1 },
      communication: { loop: false, duration: 2000, speed: 1 },
      communication_talk: { loop: false, duration: 1500, speed: 1 },
      communication_listen: { loop: true, speed: 1 },
      movement: { loop: false, duration: 1000, speed: 1 },
      movement_walk: { loop: true, speed: 1 },
      stress: { loop: true, speed: 1.5 },
      stress_warning: { loop: true, speed: 2 },
      special: { loop: false, duration: 3000, speed: 1 },
      special_celebrate: { loop: false, duration: 2000, speed: 1.5 },
    },
  },
  bob: {
    agentId: 'bob',
    defaultState: 'work_typing',
    states: {
      idle: { loop: true, speed: 1 },
      idle_normal: { loop: true, speed: 1 },
      idle_thinking: { loop: true, speed: 1 },
      work: { loop: true, speed: 1 },
      work_typing: { loop: true, speed: 2 },
      work_writing: { loop: true, speed: 1.2 },
      work_browsing: { loop: true, speed: 1 },
      communication: { loop: false, duration: 2000, speed: 1 },
      communication_talk: { loop: false, duration: 1500, speed: 1 },
      communication_listen: { loop: true, speed: 1 },
      movement: { loop: false, duration: 1000, speed: 1 },
      movement_walk: { loop: true, speed: 1 },
      stress: { loop: true, speed: 2 },
      stress_warning: { loop: true, speed: 2.5 },
      special: { loop: false, duration: 3000, speed: 1 },
      special_celebrate: { loop: false, duration: 2000, speed: 1.5 },
    },
  },
  carol: {
    agentId: 'carol',
    defaultState: 'work_browsing',
    states: {
      idle: { loop: true, speed: 1 },
      idle_normal: { loop: true, speed: 1 },
      idle_thinking: { loop: true, speed: 1 },
      work: { loop: true, speed: 1 },
      work_typing: { loop: true, speed: 1.2 },
      work_writing: { loop: true, speed: 1 },
      work_browsing: { loop: true, speed: 1.5 },
      communication: { loop: false, duration: 2000, speed: 1 },
      communication_talk: { loop: false, duration: 1500, speed: 1 },
      communication_listen: { loop: true, speed: 1 },
      movement: { loop: false, duration: 1000, speed: 1 },
      movement_walk: { loop: true, speed: 1 },
      stress: { loop: true, speed: 1.5 },
      stress_warning: { loop: true, speed: 2 },
      special: { loop: false, duration: 3000, speed: 1 },
      special_celebrate: { loop: false, duration: 2000, speed: 1.5 },
    },
  },
  dave: {
    agentId: 'dave',
    defaultState: 'idle_normal',
    states: {
      idle: { loop: true, speed: 1 },
      idle_normal: { loop: true, speed: 1 },
      idle_thinking: { loop: true, speed: 1 },
      work: { loop: true, speed: 1 },
      work_typing: { loop: true, speed: 1.5 },
      work_writing: { loop: true, speed: 1.2 },
      work_browsing: { loop: true, speed: 1 },
      communication: { loop: false, duration: 2000, speed: 1 },
      communication_talk: { loop: false, duration: 1500, speed: 1 },
      communication_listen: { loop: true, speed: 1 },
      movement: { loop: false, duration: 1000, speed: 1 },
      movement_walk: { loop: true, speed: 1 },
      stress: { loop: true, speed: 1.5 },
      stress_warning: { loop: true, speed: 2 },
      special: { loop: false, duration: 3000, speed: 1 },
      special_celebrate: { loop: false, duration: 2000, speed: 1.5 },
    },
  },
  eva: {
    agentId: 'eva',
    defaultState: 'work_browsing',
    states: {
      idle: { loop: true, speed: 1 },
      idle_normal: { loop: true, speed: 1 },
      idle_thinking: { loop: true, speed: 1 },
      work: { loop: true, speed: 1 },
      work_typing: { loop: true, speed: 1.2 },
      work_writing: { loop: true, speed: 1 },
      work_browsing: { loop: true, speed: 1.5 },
      communication: { loop: false, duration: 2000, speed: 1 },
      communication_talk: { loop: false, duration: 1500, speed: 1 },
      communication_listen: { loop: true, speed: 1 },
      movement: { loop: false, duration: 1000, speed: 1 },
      movement_walk: { loop: true, speed: 1 },
      stress: { loop: true, speed: 1.5 },
      stress_warning: { loop: true, speed: 2 },
      special: { loop: false, duration: 3000, speed: 1 },
      special_celebrate: { loop: false, duration: 2000, speed: 1.5 },
    },
  },
};

// 狀態轉換映射
export const stateTransitions: AnimationTransition[] = [
  { from: 'idle', to: 'work_typing', trigger: 'onTaskAssigned', duration: 300 },
  { from: 'work_typing', to: 'idle_thinking', trigger: 'onLLMReasoning', duration: 200 },
  { from: 'work_typing', to: 'communication_talk', trigger: 'onMessageSent', duration: 150 },
  { from: 'any', to: 'stress_warning', trigger: 'onTokenLimitWarning', duration: 100 },
  { from: 'any', to: 'special_celebrate', trigger: 'onTaskCompleted', duration: 200 },
  { from: 'idle', to: 'movement_walk', trigger: 'onMoveRequested', duration: 300 },
  { from: 'movement_walk', to: 'idle', trigger: 'onMoveComplete', duration: 200 },
];

// 根據 Agent 狀態獲取動畫狀態
export function getAnimationState(agentStatus: string): AnimationState {
  const mapping: Record<string, AnimationState> = {
    online: 'idle_normal',
    busy: 'work_typing',
    thinking: 'idle_thinking',
    offline: 'idle',
    stress: 'stress_warning',
  };
  return mapping[agentStatus] || 'idle_normal';
}

// 動畫管理器
export class AnimationManager {
  private currentStates: Record<string, AnimationState> = {};
  
  constructor() {
    // 初始化所有 Agent 狀態
    Object.keys(animationConfigs).forEach(agentId => {
      this.currentStates[agentId] = animationConfigs[agentId].defaultState;
    });
  }
  
  getState(agentId: string): AnimationState {
    return this.currentStates[agentId] || 'idle';
  }
  
  setState(agentId: string, state: AnimationState): void {
    this.currentStates[agentId] = state;
  }
  
  trigger(agentId: string, triggerEvent: string): void {
    const transitions = stateTransitions.filter(t => 
      t.from === 'any' || t.from === this.currentStates[agentId]
    );
    
    const transition = transitions.find(t => t.trigger === triggerEvent);
    if (transition) {
      this.setState(agentId, transition.to);
    }
  }
  
  getConfig(agentId: string) {
    return animationConfigs[agentId];
  }
}

export default AnimationManager;
