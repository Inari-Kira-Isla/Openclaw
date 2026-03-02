/**
 * TaskScheduler - 任務排程器
 * 支援即時/週期/事件/批次排程
 */

const { EventEmitter } = require('events');
const path = require('path');
const fs = require('fs');

class TaskScheduler extends EventEmitter {
    constructor(options = {}) {
        super();
        this.timezone = options.timezone || 'Asia/Macau';
        this.maxConcurrent = options.maxConcurrentTasks || 10;
        
        // 任務儲存
        this.tasks = new Map();           // taskId -> task
        this.scheduledJobs = new Map();   // jobName -> job config
        this.runningTasks = new Set();
        
        // 排程計時器
        this.intervals = new Map();
        this.timeouts = new Map();
        
        // 優先級隊列
        this.priorityQueue = {
            0: [], // P0: Critical
            1: [], // P1: High
            2: [], // P2: Normal
            3: []  // P3: Low
        };
        
        // 綁定上下文
        this._processQueue = this._processQueue.bind(this);
    }

    /**
     * 創建任務
     */
    createTask(taskConfig) {
        const task = {
            task_id: taskConfig.task_id || this._generateId(),
            task_type: taskConfig.task_type,
            name: taskConfig.name,
            handler: taskConfig.handler,
            priority: taskConfig.priority ?? 2,
            status: 'PENDING',
            progress: 0.0,
            created_at: new Date().toISOString(),
            started_at: null,
            completed_at: null,
            metadata: taskConfig.metadata || {},
            retry_count: 0,
            max_retries: taskConfig.max_retries || 3,
            timeout: taskConfig.timeout || 300000, // 5分鐘預設
            dependencies: taskConfig.dependencies || []
        };
        
        this.tasks.set(task.task_id, task);
        this._addToPriorityQueue(task);
        
        this.emit('task:created', task);
        return task;
    }

    /**
     * 提交任務（自動根據類型處理）
     */
    async submit(taskConfig) {
        const task = this.createTask(taskConfig);
        
        switch (taskConfig.schedule_type) {
            case 'immediate':
                return this._executeImmediate(task);
            case 'scheduled':
                return this._scheduleTask(task, taskConfig.schedule_time);
            case 'periodic':
                return this._schedulePeriodic(task, taskConfig.interval);
            case 'event':
                return this._registerEventTask(task, taskConfig.event_name);
            case 'batch':
                return this._queueBatchTask(task);
            default:
                return this._executeImmediate(task);
        }
    }

    /**
     * 立即執行任務
     */
    async _executeImmediate(task) {
        return this.executeTask(task.task_id);
    }

    /**
     * 定時執行任務
     */
    _scheduleTask(task, scheduleTime) {
        const now = new Date();
        const [hours, minutes] = scheduleTime.split(':').map(Number);
        let target = new Date(now);
        target.setHours(hours, minutes, 0, 0);
        
        // 如果時間已過，則排到明天
        if (target <= now) {
            target.setDate(target.getDate() + 1);
        }
        
        const delay = target.getTime() - now.getTime();
        
        const timeout = setTimeout(() => {
            this.executeTask(task.task_id);
            // 重新排程明天
            this._scheduleTask(task, scheduleTime);
        }, delay);
        
        this.timeouts.set(`${task.task_id}_schedule`, timeout);
        this.emit('task:scheduled', { task, executeAt: target });
        
        return { scheduled: true, nextRun: target };
    }

    /**
     * 週期性執行任務
     */
    _schedulePeriodic(task, interval) {
        // interval 可以是 cron 表達式或毫秒數
        const intervalMs = typeof interval === 'number' ? interval : this._parseInterval(interval);
        
        const runTask = () => {
            // 為週期任務創建新的執行實例
            const instance = this.createTask({
                ...task,
                task_id: `${task.task_id}_${Date.now()}`,
                metadata: { ...task.metadata, parentTaskId: task.task_id }
            });
            this.executeTask(instance.task_id);
        };
        
        const intervalId = setInterval(runTask, intervalMs);
        this.intervals.set(task.task_id, intervalId);
        
        this.emit('task:periodic_started', { task, intervalMs });
        return { scheduled: true, intervalMs };
    }

    /**
     * 事件觸發任務
     */
    _registerEventTask(task, eventName) {
        const handler = async (...args) => {
            const instance = this.createTask({
                ...task,
                task_id: `${task.task_id}_${Date.now()}`,
                metadata: { ...task.metadata, eventArgs: args, eventName }
            });
            await this.executeTask(instance.task_id);
        };
        
        this.on(eventName, handler);
        this.emit('task:event_registered', { task, eventName });
        
        return { registered: true, eventName };
    }

    /**
     * 批次任務排隊
     */
    _queueBatchTask(task) {
        task.batch = true;
        task.batch_size = task.batch_size || 100;
        this.emit('task:batch_queued', task);
        
        // 檢查是否達到批次大小
        const queue = this.priorityQueue[task.priority].filter(t => t.batch);
        if (queue.length >= task.batch_size) {
            this._executeBatch(queue);
        }
        
        return { queued: true };
    }

    /**
     * 執行批次
     */
    async _executeBatch(tasks) {
        this.emit('batch:start', { count: tasks.length });
        
        const promises = tasks.map(task => 
            this.executeTask(task.task_id).catch(err => ({ task, error: err }))
        );
        
        const results = await Promise.allSettled(promises);
        
        this.emit('batch:complete', { results });
        return results;
    }

    /**
     * 執行任務
     */
    async executeTask(taskId) {
        const task = this.tasks.get(taskId);
        if (!task) {
            throw new Error(`Task ${taskId} not found`);
        }
        
        if (task.status !== 'PENDING') {
            return task;
        }
        
        // 檢查依賴
        for (const depId of task.dependencies) {
            const dep = this.tasks.get(depId);
            if (dep && dep.status !== 'COMPLETED') {
                await this._waitForDependency(depId);
            }
        }
        
        // 檢查並發限制
        if (this.runningTasks.size >= this.maxConcurrent) {
            await this._waitForSlot();
        }
        
        // 開始執行
        task.status = 'RUNNING';
        task.started_at = new Date().toISOString();
        this.runningTasks.add(task.task_id);
        
        this.emit('task:started', task);
        
        try {
            // 執行處理器
            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Task timeout')), task.timeout)
            );
            
            const result = await Promise.race([
                task.handler(task),
                timeoutPromise
            ]);
            
            // 完成任務
            task.status = 'COMPLETED';
            task.progress = 1.0;
            task.completed_at = new Date().toISOString();
            task.result = result;
            
            this.emit('task:completed', task);
            
        } catch (error) {
            await this._handleTaskError(task, error);
        } finally {
            this.runningTasks.delete(task.task_id);
            this.emit('task:removed_from_queue', task);
        }
        
        return task;
    }

    /**
     * 處理任務錯誤
     */
    async _handleTaskError(task, error) {
        task.retry_count++;
        task.last_error = error.message;
        
        if (task.retry_count < task.max_retries) {
            // 指數退避重試
            const delay = Math.pow(2, task.retry_count) * 1000;
            task.status = 'PENDING';
            task.progress = 0;
            
            this.emit('task:retrying', { task, retryCount: task.retry_count, delay });
            
            await new Promise(resolve => setTimeout(resolve, delay));
            return this.executeTask(task.task_id);
        }
        
        task.status = 'FAILED';
        task.completed_at = new Date().toISOString();
        task.error = error.message;
        
        this.emit('task:failed', task);
    }

    /**
     * 取消任務
     */
    cancelTask(taskId) {
        const task = this.tasks.get(taskId);
        if (!task) return false;
        
        if (task.status === 'RUNNING') {
            // 標記為取消，下一次檢查時會停止
            task.cancelled = true;
        }
        
        task.status = 'CANCELLED';
        task.completed_at = new Date().toISOString();
        
        // 清理定時器
        if (this.intervals.has(taskId)) {
            clearInterval(this.intervals.get(taskId));
            this.intervals.delete(taskId);
        }
        
        this._removeFromPriorityQueue(task);
        this.emit('task:cancelled', task);
        
        return true;
    }

    /**
     * 獲取任務狀態
     */
    getTask(taskId) {
        return this.tasks.get(taskId);
    }

    /**
     * 獲取所有任務
     */
    getAllTasks(status) {
        const all = Array.from(this.tasks.values());
        if (status) {
            return all.filter(t => t.status === status);
        }
        return all;
    }

    /**
     * 設置定時任務（簡化配置介面）
     */
    scheduleCron(name, config) {
        const { time, task, handler } = config;
        
        // 解析時間 (HH:MM,HH:MM,...)
        const times = time.split(',');
        
        times.forEach((t, index) => {
            const jobId = `${name}_${index}`;
            
            const job = {
                name: jobId,
                originalName: name,
                time: t,
                task_type: task,
                handler,
                scheduled: true
            };
            
            this.scheduledJobs.set(jobId, job);
            
            // 計算下次執行時間
            this._scheduleCronJob(job);
        });
        
        this.emit('scheduler:cron_configured', { name, times });
    }

    /**
     * 排程 Cron 任務
     */
    _scheduleCronJob(job) {
        const [hours, minutes] = job.time.split(':').map(Number);
        
        const scheduleNext = () => {
            const now = new Date();
            const target = new Date(now);
            target.setHours(hours, minutes, 0, 0);
            
            if (target <= now) {
                target.setDate(target.getDate() + 1);
            }
            
            const delay = target.getTime() - now.getTime();
            
            const timeout = setTimeout(async () => {
                // 執行任務
                if (job.handler) {
                    await job.handler({ time: job.time, triggeredAt: target });
                }
                
                this.emit('scheduler:cron_triggered', job);
                
                // 排程下一次
                scheduleNext();
            }, delay);
            
            this.timeouts.set(`cron_${job.name}`, timeout);
        };
        
        scheduleNext();
    }

    /**
     * 停止排程器
     */
    shutdown() {
        // 清除所有定時器
        for (const [id, timeout] of this.timeouts) {
            clearTimeout(timeout);
        }
        for (const [id, interval] of this.intervals) {
            clearInterval(interval);
        }
        
        this.timeouts.clear();
        this.intervals.clear();
        
        this.emit('scheduler:shutdown');
    }

    // 私有方法
    
    _generateId() {
        return `slm_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    _parseInterval(interval) {
        // 支援 "6h", "30m", "1h30m" 等格式
        const match = interval.match(/(\d+)([hms])/);
        if (!match) return 60000;
        
        const value = parseInt(match[1]);
        const unit = match[2];
        
        const multipliers = { h: 3600000, m: 60000, s: 1000 };
        return value * (multipliers[unit] || 60000);
    }

    _addToPriorityQueue(task) {
        this.priorityQueue[task.priority].push(task);
    }

    _removeFromPriorityQueue(task) {
        const queue = this.priorityQueue[task.priority];
        const index = queue.findIndex(t => t.task_id === task.task_id);
        if (index > -1) queue.splice(index, 1);
    }

    async _waitForDependency(depId) {
        return new Promise(resolve => {
            const check = () => {
                const dep = this.tasks.get(depId);
                if (dep && dep.status === 'COMPLETED') {
                    resolve();
                } else {
                    setTimeout(check, 100);
                }
            };
            check();
        });
    }

    async _waitForSlot() {
        return new Promise(resolve => {
            const check = () => {
                if (this.runningTasks.size < this.maxConcurrent) {
                    resolve();
                } else {
                    setTimeout(check, 100);
                }
            };
            check();
        });
    }

    _processQueue() {
        // 處理優先級隊列
        for (let p = 0; p <= 3; p++) {
            const queue = this.priorityQueue[p];
            while (queue.length > 0 && this.runningTasks.size < this.maxConcurrent) {
                const task = queue.shift();
                if (task.status === 'PENDING') {
                    this.executeTask(task.task_id);
                }
            }
        }
    }
}

module.exports = TaskScheduler;
