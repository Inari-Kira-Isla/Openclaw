/**
 * StateManager - 狀態管理器
 * 狀態機：PENDING → RUNNING → COMPLETED/FAILED/CANCELLED
 * 持久化狀態到 JSON 檔
 */

const fs = require('fs');
const path = require('path');
const { EventEmitter } = require('events');

// 任務狀態枚舉
const TaskStatus = {
    PENDING: 'PENDING',
    RUNNING: 'RUNNING',
    COMPLETED: 'COMPLETED',
    FAILED: 'FAILED',
    CANCELLED: 'CANCELLED'
};

// 優先級常量
const Priority = {
    CRITICAL: 0,  // P0: 即時學習反饋、錯誤修正
    HIGH: 1,     // P1: 定期複習、記憶鞏固
    NORMAL: 2,   // P2: 知識整合、模式識別
    LOW: 3       // P3: 長期優化、效能調校
};

class StateManager extends EventEmitter {
    constructor(options = {}) {
        super();
        
        this.storagePath = options.storagePath || 
            path.join(process.env.HOME || '.', '.openclaw', 'workspace', 'slime-system', 'data');
        this.stateFile = options.stateFile || 'task-states.json';
        this.autoSave = options.autoSave ?? true;
        this.saveInterval = options.saveInterval || 5000; // 5秒自動儲存
        
        // 記憶體狀態
        this.states = new Map();        // taskId -> state
        this.history = [];              // 狀態變更歷史
        this.maxHistory = options.maxHistory || 1000;
        
        // 確保存儲目錄存在
        this._ensureStorageDir();
        
        // 自動儲存計時器
        if (this.autoSave) {
            this._saveTimer = setInterval(() => this._autoSave(), this.saveInterval);
        }
        
        // 載入已有狀態
        this._loadStates();
    }

    /**
     * 確保存儲目錄存在
     */
    _ensureStorageDir() {
        if (!fs.existsSync(this.storagePath)) {
            fs.mkdirSync(this.storagePath, { recursive: true });
        }
    }

    /**
     * 獲取狀態文件路徑
     */
    _getStateFilePath() {
        return path.join(this.storagePath, this.stateFile);
    }

    /**
     * 載入狀態
     */
    _loadStates() {
        const filePath = this._getStateFilePath();
        
        try {
            if (fs.existsSync(filePath)) {
                const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
                
                if (data.states) {
                    for (const [taskId, state] of Object.entries(data.states)) {
                        this.states.set(taskId, state);
                    }
                }
                
                if (data.history) {
                    this.history = data.history;
                }
                
                this.emit('states:loaded', { count: this.states.size });
            }
        } catch (error) {
            console.error('Failed to load states:', error);
            this.emit('states:load_error', error);
        }
    }

    /**
     * 儲存狀態
     */
    saveStates() {
        const filePath = this._getStateFilePath();
        
        const data = {
            version: '1.0',
            saved_at: new Date().toISOString(),
            states: Object.fromEntries(this.states),
            history: this.history.slice(-this.maxHistory)
        };
        
        try {
            fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
            this.emit('states:saved', { count: this.states.size });
            return true;
        } catch (error) {
            console.error('Failed to save states:', error);
            this.emit('states:save_error', error);
            return false;
        }
    }

    /**
     * 自動儲存
     */
    _autoSave() {
        if (this._dirty) {
            this.saveStates();
            this._dirty = false;
        }
    }

    /**
     * 標記為髒（需要儲存）
     */
    _markDirty() {
        this._dirty = true;
    }

    /**
     * 創建新狀態
     */
    createState(taskId, taskType, metadata = {}) {
        const state = {
            task_id: taskId,
            task_type: taskType,
            status: TaskStatus.PENDING,
            priority: metadata.priority ?? Priority.NORMAL,
            progress: 0.0,
            created_at: new Date().toISOString(),
            started_at: null,
            completed_at: null,
            metadata: metadata,
            retry_count: 0,
            error: null,
            result: null
        };
        
        this.states.set(taskId, state);
        this._addHistory(taskId, 'CREATED', state);
        this._markDirty();
        
        this.emit('state:created', state);
        return state;
    }

    /**
     * 獲取狀態
     */
    getState(taskId) {
        return this.states.get(taskId) || null;
    }

    /**
     * 獲取所有狀態
     */
    getAllStates(status = null) {
        const all = Array.from(this.states.values());
        if (status) {
            return all.filter(s => s.status === status);
        }
        return all;
    }

    /**
     * 獲取待處理任務
     */
    getPendingTasks() {
        return this.getAllStates(TaskStatus.PENDING)
            .sort((a, b) => a.priority - b.priority);
    }

    /**
     * 獲取運行中任務
     */
    getRunningTasks() {
        return this.getAllStates(TaskStatus.RUNNING);
    }

    /**
     * 開始任務
     */
    startTask(taskId, metadata = {}) {
        const state = this.states.get(taskId);
        if (!state) {
            throw new Error(`State for task ${taskId} not found`);
        }
        
        if (state.status !== TaskStatus.PENDING) {
            throw new Error(`Cannot start task in status: ${state.status}`);
        }
        
        state.status = TaskStatus.RUNNING;
        state.started_at = new Date().toISOString();
        state.progress = 0.0;
        
        if (metadata) {
            state.metadata = { ...state.metadata, ...metadata };
        }
        
        this._addHistory(taskId, 'STARTED', state);
        this._markDirty();
        
        this.emit('state:started', state);
        return state;
    }

    /**
     * 更新進度
     */
    updateProgress(taskId, progress) {
        const state = this.states.get(taskId);
        if (!state) return null;
        
        state.progress = Math.max(0, Math.min(1, progress));
        
        this._addHistory(taskId, 'PROGRESS', state);
        this._markDirty();
        
        this.emit('state:progress', state);
        return state;
    }

    /**
     * 完成任務
     */
    completeTask(taskId, result = null) {
        const state = this.states.get(taskId);
        if (!state) {
            throw new Error(`State for task ${taskId} not found`);
        }
        
        state.status = TaskStatus.COMPLETED;
        state.completed_at = new Date().toISOString();
        state.progress = 1.0;
        state.result = result;
        
        this._addHistory(taskId, 'COMPLETED', state);
        this._markDirty();
        
        this.emit('state:completed', state);
        return state;
    }

    /**
     * 失敗任務
     */
    failTask(taskId, error, retryable = true) {
        const state = this.states.get(taskId);
        if (!state) {
            throw new Error(`State for task ${taskId} not found`);
        }
        
        state.retry_count++;
        state.error = error;
        
        if (retryable && state.retry_count < (state.metadata.max_retries || 3)) {
            // 可重試，回到 PENDING
            state.status = TaskStatus.PENDING;
            state.progress = 0;
            
            this._addHistory(taskId, 'RETRY', state);
            this.emit('state:retry', state);
        } else {
            // 不可重試或達到最大重試次數
            state.status = TaskStatus.FAILED;
            state.completed_at = new Date().toISOString();
            
            this._addHistory(taskId, 'FAILED', state);
            this.emit('state:failed', state);
        }
        
        this._markDirty();
        return state;
    }

    /**
     * 取消任務
     */
    cancelTask(taskId) {
        const state = this.states.get(taskId);
        if (!state) {
            throw new Error(`State for task ${taskId} not found`);
        }
        
        if (state.status === TaskStatus.RUNNING) {
            // 標記為需要取消，實際取消由調用者處理
            state.cancelled = true;
        }
        
        state.status = TaskStatus.CANCELLED;
        state.completed_at = new Date().toISOString();
        
        this._addHistory(taskId, 'CANCELLED', state);
        this._markDirty();
        
        this.emit('state:cancelled', state);
        return state;
    }

    /**
     * 更新元數據
     */
    updateMetadata(taskId, metadata) {
        const state = this.states.get(taskId);
        if (!state) return null;
        
        state.metadata = { ...state.metadata, ...metadata };
        this._markDirty();
        
        this.emit('state:metadata_updated', state);
        return state;
    }

    /**
     * 刪除狀態
     */
    deleteState(taskId) {
        const state = this.states.get(taskId);
        if (!state) return false;
        
        this.states.delete(taskId);
        this._addHistory(taskId, 'DELETED', { taskId });
        this._markDirty();
        
        this.emit('state:deleted', { taskId });
        return true;
    }

    /**
     * 清理歷史
     */
    cleanHistory(beforeDate = null) {
        const cutoff = beforeDate ? new Date(beforeDate) : new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
        
        const before = this.history.length;
        this.history = this.history.filter(h => new Date(h.timestamp) > cutoff);
        
        const cleaned = before - this.history.length;
        this.emit('history:cleaned', { cleaned, remaining: this.history.length });
        
        return cleaned;
    }

    /**
     * 獲取統計信息
     */
    getStats() {
        const all = Array.from(this.states.values());
        
        const stats = {
            total: all.length,
            by_status: {},
            by_type: {},
            by_priority: {},
            avg_duration_ms: 0,
            success_rate: 0
        };
        
        // 按狀態統計
        for (const status of Object.values(TaskStatus)) {
            stats.by_status[status] = all.filter(s => s.status === status).length;
        }
        
        // 按類型統計
        const typeMap = new Map();
        for (const state of all) {
            const type = state.task_type;
            typeMap.set(type, (typeMap.get(type) || 0) + 1);
        }
        stats.by_type = Object.fromEntries(typeMap);
        
        // 按優先級統計
        for (let p = 0; p <= 3; p++) {
            stats.by_priority[p] = all.filter(s => s.priority === p).length;
        }
        
        // 計算平均執行時間
        const completed = all.filter(s => s.status === TaskStatus.COMPLETED && s.started_at && s.completed_at);
        if (completed.length > 0) {
            const totalDuration = completed.reduce((sum, s) => {
                return sum + (new Date(s.completed_at) - new Date(s.started_at));
            }, 0);
            stats.avg_duration_ms = totalDuration / completed.length;
        }
        
        // 計算成功率
        const finished = all.filter(s => s.status === TaskStatus.COMPLETED || s.status === TaskStatus.FAILED);
        if (finished.length > 0) {
            stats.success_rate = stats.by_status[TaskStatus.COMPLETED] / finished.length;
        }
        
        return stats;
    }

    /**
     * 導出狀態
     */
    exportStates(format = 'json') {
        const data = {
            exported_at: new Date().toISOString(),
            stats: this.getStats(),
            states: Object.fromEntries(this.states)
        };
        
        if (format === 'json') {
            return JSON.stringify(data, null, 2);
        }
        
        return data;
    }

    /**
     * 添加歷史記錄
     */
    _addHistory(taskId, event, data) {
        this.history.push({
            task_id: taskId,
            event,
            timestamp: new Date().toISOString(),
            data: { ...data }
        });
        
        // 限制歷史長度
        if (this.history.length > this.maxHistory) {
            this.history = this.history.slice(-this.maxHistory);
        }
    }

    /**
     * 獲取歷史
     */
    getHistory(taskId = null, limit = 100) {
        if (taskId) {
            return this.history
                .filter(h => h.task_id === taskId)
                .slice(-limit);
        }
        
        return this.history.slice(-limit);
    }

    /**
     * 關閉並儲存
     */
    shutdown() {
        if (this._saveTimer) {
            clearInterval(this._saveTimer);
        }
        
        this.saveStates();
        this.emit('manager:shutdown');
    }
}

// 導出常量和類
module.exports = {
    StateManager,
    TaskStatus,
    Priority
};
