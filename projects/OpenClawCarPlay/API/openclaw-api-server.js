// OpenClaw API Server - Express.js
// 這是需要安裝在 OpenClaw 系統中的 API Server

const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// Configuration
const CONFIG = {
    port: process.env.PORT || 8080,
    userID: 'carplay-ios'
};

// In-memory storage (replace with database)
let tasks = [];
let schedule = [];
let conversationHistory = [];

// Routes

// 1. Ping
app.get('/api/ping', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 2. Voice Message
app.post('/api/voice', async (req, res) => {
    const { text, userID } = req.body;
    
    // Store in history
    conversationHistory.push({
        user: text,
        timestamp: new Date().toISOString()
    });
    
    // Process command
    const response = await processCommand(text);
    
    res.json({
        success: true,
        message: response,
        timestamp: new Date().toISOString()
    });
});

// 3. Search
app.post('/api/search', async (req, res) => {
    const { query, userID } = req.body;
    
    // TODO: Integrate with web search
    const results = await performSearch(query);
    
    res.json({
        success: true,
        message: `搜尋結果：${results.join(', ')}`,
        data: { results }
    });
});

// 4. Music
app.post('/api/music', (req, res) => {
    const { command, userID } = req.body;
    
    const musicCommands = {
        'play': '正在播放音樂',
        'pause': '已暫停',
        'next': '已切換到下一首',
        'previous': '已切換到上一首',
        'shuffle': '已開啟隨機播放'
    };
    
    res.json({
        success: true,
        message: musicCommands[command] || '未知指令'
    });
});

// 5. Tasks
app.post('/api/task', (req, res) => {
    const { command, title, taskID, userID } = req.body;
    
    switch (command) {
        case 'create':
            const newTask = {
                id: Date.now().toString(),
                title,
                status: 'pending',
                createdAt: new Date().toISOString()
            };
            tasks.push(newTask);
            res.json({
                success: true,
                message: `已建立任務：${title}`,
                data: { task: newTask }
            });
            break;
            
        case 'list':
            res.json({
                success: true,
                message: `共有 ${tasks.length} 個任務`,
                data: { tasks }
            });
            break;
            
        case 'complete':
            const taskIndex = tasks.findIndex(t => t.id === taskID);
            if (taskIndex >= 0) {
                tasks[taskIndex].status = 'completed';
                res.json({
                    success: true,
                    message: '任務已完成',
                    data: { task: tasks[taskIndex] }
                });
            } else {
                res.json({ success: false, message: '找不到任務' });
            }
            break;
            
        default:
            res.json({ success: false, message: '未知指令' });
    }
});

// 6. Schedule
app.post('/api/schedule', (req, res) => {
    const { command, date, userID } = req.body;
    
    // Return mock schedule
    const mockSchedule = [
        { time: '09:00', title: '會議', location: '辦公室' },
        { time: '14:00', title: '午餐', location: '餐廳' }
    ];
    
    res.json({
        success: true,
        message: `今日有 ${mockSchedule.length} 個日程`,
        data: { schedule: mockSchedule }
    });
});

// Command Processor
async function processCommand(text) {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('天氣')) {
        return '今天天氣晴朗，溫度 22 度';
    }
    
    if (lowerText.includes('任務')) {
        return `目前有 ${tasks.length} 個任務`;
    }
    
    if (lowerText.includes('音樂') || lowerText.includes('播放')) {
        return '正在播放音樂';
    }
    
    if (lowerText.includes('日程') || lowerText.includes('行程')) {
        return '今天的行程：早上 9 點會議，下午 2 點午餐';
    }
    
    // Default: Echo with processing
    return `收到：${text}。我正在處理中...`;
}

// Search Function
async function performSearch(query) {
    // TODO: Integrate with actual search API
    return [
        '結果 1: ' + query + ' - 相關資訊',
        '結果 2: ' + query + ' - 維基百科',
        '結果 3: ' + query + ' - 新聞報導'
    ];
}

// Start Server
app.listen(CONFIG.port, () => {
    console.log(`OpenClaw API Server running on port ${CONFIG.port}`);
});

module.exports = app;
