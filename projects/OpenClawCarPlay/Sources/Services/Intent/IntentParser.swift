import Foundation

/// Intent Parser - Routes voice commands to the right handler
class IntentParser {
    
    // MARK: - Command Types
    
    enum CommandType {
        case controlPhone   // Open apps, make calls
        case music         // Play, pause, next, search
        case task          // Create, list, update tasks
        case search        // Web search
        case aiChat        // General AI conversation
        case schedule      // Calendar, reminders
        case unknown
    }
    
    struct ParsedIntent {
        let type: CommandType
        let action: String
        let parameters: [String: String]
        let rawText: String
    }
    
    // MARK: - Parse
    
    func parse(_ text: String) -> ParsedIntent {
        let lowercased = text.lowercased()
        
        // Phone control commands
        if isPhoneControl(lc: lowercased) {
            return ParsedIntent(
                type: .controlPhone,
                action: extractPhoneAction(lc: lowercased),
                parameters: extractPhoneParams(text: text),
                rawText: text
            )
        }
        
        // Music commands
        if isMusicCommand(lc: lowercased) {
            return ParsedIntent(
                type: .music,
                action: extractMusicAction(lc: lowercased),
                parameters: extractMusicParams(text: text),
                rawText: text
            )
        }
        
        // Task commands
        if isTaskCommand(lc: lowercased) {
            return ParsedIntent(
                type: .task,
                action: extractTaskAction(lc: lowercased),
                parameters: extractTaskParams(text: text),
                rawText: text
            )
        }
        
        // Search commands
        if isSearchCommand(lc: lowercased) {
            return ParsedIntent(
                type: .search,
                action: "search",
                parameters: ["query": extractSearchQuery(text: text)],
                rawText: text
            )
        }
        
        // Schedule commands
        if isScheduleCommand(lc: lowercased) {
            return ParsedIntent(
                type: .schedule,
                action: extractScheduleAction(lc: lowercased),
                parameters: extractScheduleParams(text: text),
                rawText: text
            )
        }
        
        // Default: AI chat
        return ParsedIntent(
            type: .aiChat,
            action: "chat",
            parameters: ["message": text],
            rawText: text
        )
    }
    
    // MARK: - Phone Control Detection
    
    private func isPhoneControl(lc: String) -> Bool {
        let keywords = ["打開", "打開", "開", "開啟", "打電話", "call", "open", "訊息", "message"]
        return keywords.contains { lc.contains($0) }
    }
    
    private func extractPhoneAction(lc: String) -> String {
        if lc.contains("電話") || lc.contains("call") { return "call" }
        if lc.contains("訊息") || lc.contains("message") { return "message" }
        if lc.contains("音樂") || lc.contains("music") { return "music" }
        if lc.contains("地圖") || lc.contains("map") { return "maps" }
        if lc.contains("日曆") || lc.contains("calendar") { return "calendar" }
        if lc.contains("提醒") || lc.contains("reminder") { return "reminder" }
        return "open"
    }
    
    private func extractPhoneParams(text: String) -> [String: String] {
        // Extract phone number or app name
        return [:]
    }
    
    // MARK: - Music Detection
    
    private func isMusicCommand(lc: String) -> Bool {
        let keywords = ["音樂", "播放", "暫停", "下一首", "上一首", "music", "play", "pause", "next", "previous"]
        return keywords.contains { lc.contains($0) }
    }
    
    private func extractMusicAction(lc: String) -> String {
        if lc.contains("播放") || lc.contains("play") { return "play" }
        if lc.contains("暫停") || lc.contains("pause") || lc.contains("停止") { return "pause" }
        if lc.contains("下一首") || lc.contains("next") { return "next" }
        if lc.contains("上一首") || lc.contains("previous") { return "previous" }
        if lc.contains("隨機") || lc.contains("shuffle") { return "shuffle" }
        if lc.contains("搜尋") || lc.contains("search") { return "search" }
        return "play"
    }
    
    private func extractMusicParams(text: String) -> [String: String] {
        // Extract song/artist name
        return [:]
    }
    
    // MARK: - Task Detection
    
    private func isTaskCommand(lc: String) -> Bool {
        let keywords = ["任務", "待辦", "工作", "task", "todo", "完成"]
        return keywords.contains { lc.contains($0) }
    }
    
    private func extractTaskAction(lc: String) -> String {
        if lc.contains("新增") || lc.contains("建立") || lc.contains("create") || lc.contains("加") { return "create" }
        if lc.contains("完成") || lc.contains("done") || lc.contains("finish") { return "complete" }
        if lc.contains("列表") || lc.contains("list") || lc.contains("查看") { return "list" }
        if lc.contains("刪除") || lc.contains("delete") || lc.contains("移除") { return "delete" }
        return "list"
    }
    
    private func extractTaskParams(text: String) -> [String: String] {
        // Extract task title
        return [:]
    }
    
    // MARK: - Search Detection
    
    private func isSearchCommand(lc: String) -> Bool {
        let keywords = ["搜尋", "查", "找", "search", "google"]
        return keywords.contains { lc.contains($0) }
    }
    
    private func extractSearchQuery(text: String) -> String {
        // Extract query from "搜尋XXX"
        return text
    }
    
    // MARK: - Schedule Detection
    
    private func isScheduleCommand(lc: String) -> Bool {
        let keywords = ["日曆", "日程", "行程", "calendar", "schedule", "會議", "meeting"]
        return keywords.contains { lc.contains($0) }
    }
    
    private func extractScheduleAction(lc: String) -> String {
        if lc.contains("新增") || lc.contains("建立") || lc.contains("add") { return "add" }
        if lc.contains("查") || lc.contains("看") || lc.contains("list") { return "list" }
        return "list"
    }
    
    private func extractScheduleParams(text: String) -> [String: String] {
        return [:]
    }
}

// MARK: - Intent Handler Router

class IntentRouter {
    let parser = IntentParser()
    let phoneController = PhoneAppController()
    let musicManager = MusicManager()
    let tts = TTSManager()
    
    func handle(_ text: String, aiResponse: @escaping (String) -> Void) {
        let intent = parser.parse(text)
        
        switch intent.type {
        case .controlPhone:
            let response = phoneController.handleCommand(text)
            aiResponse(response)
            
        case .music:
            handleMusic(intent.action, text: text, response: aiResponse)
            
        case .task:
            // Call OpenClaw API for task management
            aiResponse("正在處理任務...")
            
        case .search:
            // Call OpenClaw API for search
            aiResponse("正在搜尋...")
            
        case .schedule:
            // Call OpenClaw API for schedule
            aiResponse("正在查詢日程...")
            
        case .aiChat, .unknown:
            // Let AI handle it
            aiResponse("我來處理...")
        }
    }
    
    private func handleMusic(_ action: String, text: String, response: @escaping (String) -> Void) {
        switch action {
        case "play":
            musicManager.play()
            response("正在播放音樂")
        case "pause":
            musicManager.pause()
            response("已暫停")
        case "next":
            musicManager.nextTrack()
            response("已切換到下一首")
        case "previous":
            musicManager.previousTrack()
            response("已切換到上一首")
        case "search":
            // Extract song name and search
            musicManager.searchAndPlay(query: text)
            response("正在搜尋並播放")
        default:
            response("無法識別音樂指令")
        }
    }
}
