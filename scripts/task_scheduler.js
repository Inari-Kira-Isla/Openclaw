/**
 * 調度系統 - Task Scheduler
 * 任務優先級排程
 */

const PRIORITY = {
  CRITICAL: 1,
  HIGH: 2,
  MEDIUM: 3,
  LOW: 4
};

class TaskScheduler {
  constructor() {
    this.tasks = [];
    this.running = false;
  }
  
  addTask(name, fn, priority = PRIORITY.MEDIUM) {
    this.tasks.push({
      name,
      fn,
      priority,
      status: 'pending',
      createdAt: new Date()
    });
    
    // Sort by priority
    this.tasks.sort((a, b) => a.priority - b.priority);
    
    return this.tasks.length;
  }
  
  async executeAll() {
    this.running = true;
    const results = [];
    
    for (const task of this.tasks) {
      if (task.status === 'pending') {
        task.status = 'running';
        try {
          await task.fn();
          task.status = 'completed';
        } catch (e) {
          task.status = 'failed';
          task.error = e.message;
        }
      }
    }
    
    this.running = false;
    return results;
  }
  
  getStatus() {
    return {
      total: this.tasks.length,
      pending: this.tasks.filter(t => t.status === 'pending').length,
      running: this.tasks.filter(t => t.status === 'running').length,
      completed: this.tasks.filter(t => t.status === 'completed').length,
      failed: this.tasks.filter(t => t.status === 'failed').length
    };
  }
}

module.exports = new TaskScheduler();
