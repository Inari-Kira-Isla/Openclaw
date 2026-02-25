// OpenClaw API Server - Express.js
// 更新版本：整合 carplay.sh 語音功能

const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const app = express();

app.use(cors());
app.use(express.json());

// Configuration
const CONFIG = {
    port: process.env.PORT || 8080,
    userID: 'carplay-ios',
    voiceScript: '/Users/ki/.openclaw/workspace/projects/OpenClawCarPlay/carplay.sh'
};

// In-memory storage
let tasks = [];
let schedule = [];
let conversationHistory = [];

// ==================== 語音功能 ====================

// 執行 carplay.sh 腳本
function runVoiceScript(command, args) {
    return new Promise((resolve, reject) => {
        const scriptPath = CONFIG.voiceScript;
        exec(`${scriptPath} ${command} "${args}"`, (error, stdout, stderr) => {
            if (error) {
                reject(error);
            } else {
                resolve(stdout);
            }
        });
    });
}

// ==================== API Endpoints ====================

// 1. Ping
app.get('/api/ping', (req, res) => {
    res.json({ 
        status: 'ok', 
        timestamp: new Date().toISOString(),
        carplay: 'connected'
    });
});

// 2. 取得連線狀態
app.get('/api/status', async (req, res) => {
    try {
        const voiceResult = await runVoiceScript('get-voice', '');
        res.json({
            status: 'ok',
            voice: voiceResult.trim(),
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.json({
            status: 'ok',
            voice: 'default',
            timestamp: new Date().toISOString()
        });
    }
});

// 3. 設定語音
app.post('/api/voice/set', async (req, res) => {
    const { voice } = req.body;
    try {
        await runVoiceScript('set-voice', voice);
        res.json({ success: true, voice: voice });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 4. 列出可用語音
app.get('/api/voice/list', (req, res) => {
    exec(`${CONFIG.voiceScript} voices`, (error, stdout, stderr) => {
        if (error) {
            res.json({ voices: ['Meijia', 'Tingting'] });
        } else {
            res.json({ voices: stdout.split('\n').filter(v => v.trim()) });
        }
    });
});

// 5. 任務完成通知 (NEW!)
app.post('/api/task-complete', async (req, res) => {
    const { taskName, details } = req.body;
    
    try {
        // 觸發語音通知
        await runVoiceScript('notify', taskName || '任務完成');
        
        res.json({
            success: true,
            message: `任務通知已發送: ${taskName}`,
            voice: true
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 6. 語音回覆 (NEW!)
app.post('/api/voice-reply', async (req, res) => {
    const { message, type } = req.body;
    
    try {
        // 根據類型選擇語音
        const command = type === 'error' ? 'error' : 'reply';
        await runVoiceScript(command, message);
        
        res.json({
            success: true,
            message: message,
            voice: true
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 7. 測試語音
app.post('/api/voice/test', async (req, res) => {
    const { text } = req.body;
    
    try {
        await runVoiceScript('reply', text || '測試成功');
        res.json({ success: true, message: '語音測試完成' });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 8. Voice Message
app.post('/api/voice', async (req, res) => {
    const { text, userID } = req.body;
    
    conversationHistory.push({
        user: text,
        timestamp: new Date().toISOString()
    });
    
    // 處理命令
    const response = await processCommand(text);
    
    // 語音回覆
    try {
        await runVoiceScript('reply', response);
    } catch (e) {
        console.log('語音回覆失敗:', e);
    }
    
    res.json({
        success: true,
        message: response,
        timestamp: new Date().toISOString()
    });
});

// 9. Search
app.post('/api/search', async (req, res) => {
    const { query } = req.body;
    
    try {
        const result = await runVoiceScript('reply', `搜尋結果：${query}`);
        res.json({
            success: true,
            results: result,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 10. Music Control
app.post('/api/music', async (req, res) => {
    const { action, track } = req.body;
    
    let response = '';
    switch(action) {
        case 'play':
            response = '正在播放音樂';
            break;
        case 'pause':
            response = '已暫停';
            break;
        case 'next':
            response = '切換下一首';
            break;
        case 'previous':
            response = '切換上一首';
            break;
        default:
            response = '未知指令';
    }
    
    // 語音回覆
    await runVoiceScript('reply', response);
    
    res.json({
        success: true,
        message: response,
        timestamp: new Date().toISOString()
    });
});

// 11. Tasks
app.get('/api/tasks', (req, res) => {
    res.json({ tasks });
});

app.post('/api/tasks', (req, res) => {
    const { title, description } = req.body;
    const task = {
        id: Date.now(),
        title,
        description,
        completed: false,
        createdAt: new Date().toISOString()
    };
    tasks.push(task);
    res.json({ success: true, task });
});

// 12. Schedule
app.get('/api/schedule', (req, res) => {
    res.json({ schedule });
});

app.post('/api/schedule', (req, res) => {
    const { title, time, description } = req.body;
    const event = {
        id: Date.now(),
        title,
        time,
        description,
        createdAt: new Date().toISOString()
    };
    schedule.push(event);
    res.json({ success: true, event });
});

// Command Processor
async function processCommand(text) {
    if (text.includes('天氣')) {
        return '今天天氣晴朗，溫度適中';
    } else if (text.includes('任務')) {
        return '你有 3 個待辦任務';
    } else if (text.includes('行程') || text.includes('日程')) {
        return '今天沒有其他行程';
    } else if (text.includes('音樂')) {
        return '正在播放音樂';
    } else {
        return '我收到了：' + text;
    }
}

// Start Server
const PORT = CONFIG.port;
app.listen(PORT, () => {
    console.log(`🚀 OpenClaw CarPlay API Server running on port ${PORT}`);
    console.log(`📱 Voice script: ${CONFIG.voiceScript}`);
});

module.exports = app;
