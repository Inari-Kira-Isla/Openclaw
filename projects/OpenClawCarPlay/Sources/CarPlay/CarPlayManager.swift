import CarPlay
import SwiftUI

class CarPlaySceneDelegate: UIResponder, CPTemplateApplicationSceneDelegate {
    
    var interfaceController: CPTemplateApplicationSceneController?
    var voiceCommandHandler: ((String) -> Void)?
    
    // MARK: - CPTemplateApplicationSceneDelegate
    
    func templateApplicationScene(_ templateApplicationScene: CPTemplateApplicationScene,
                                  didConnect interfaceController: CPTemplateApplicationSceneController) {
        self.interfaceController = interfaceController
        
        // Create main tab bar interface
        let rootTemplate = createRootTemplate()
        interfaceController.setRootTemplate(rootTemplate, animated: true, completion: nil)
        
        // Notify app that CarPlay is connected
        NotificationCenter.default.post(name: .carPlayConnected, object: nil)
    }
    
    func templateApplicationScene(_ templateApplicationScene: CPTemplateApplicationScene,
                                  didDisconnectInterfaceController interfaceController: CPTemplateApplicationSceneInterfaceController) {
        self.interfaceController = nil
        NotificationCenter.default.post(name: .carPlayDisconnected, object: nil)
    }
    
    // MARK: - Template Creation
    
    private func createRootTemplate() -> CPTemplate {
        // Main tab bar with 4 tabs
        let tabBar = CPTabBarTemplate(templates: [
            createHomeTemplate(),
            createVoiceTemplate(),
            createMusicTemplate(),
            createTasksTemplate()
        ])
        
        tabBar.selectedTemplateIndex = 1 // Start on voice
        
        return tabBar
    }
    
    // MARK: - Home Template (快速指令)
    
    private func createHomeTemplate() -> CPTemplate {
        let home = CPHomeTemplate()
        
        // Quick actions - displayed on home screen
        var quickActions: [CPQuickAction] = [
            CPQuickAction(title: "🔍 搜尋", image: UIImage(systemName: "magnifyingglass"), handler: { [weak self] _ in
                self?.switchToVoice()
            }),
            CPQuickAction(title: "📋 任務", image: UIImage(systemName: "checklist"), handler: { [weak self] _ in
                self?.switchToTasks()
            }),
            CPQuickAction(title: "🎵 音樂", image: UIImage(systemName: "music.note"), handler: { [weak self] _ in
                self?.switchToMusic()
            }),
            CPQuickAction(title: "📅 日程", image: UIImage(systemName: "calendar"), handler: { [weak self] _ in
                self?.showSchedule()
            })
        ]
        
        home.quickActions = quickActions
        home.tabImage = UIImage(systemName: "house.fill")
        
        return home
    }
    
    // MARK: - Voice Template (語音控制 - 主要)
    
    private func createVoiceTemplate() -> CPTemplate {
        // Create voice control template
        let voice = CPVoiceControlTemplate(titleVariants: ["OpenClaw 語音助手"])
        
        // Voice control buttons
        voice.voiceControlStates = [
            CPVoiceControlState(
                titleVariants: ["說話"],
                imageVariants: [UIImage(systemName: "mic.fill")!],
                isActive: true,
                enabled: true
            )
        ]
        
        // Add voice button to template
        let button = CPVoiceControlButton(
            imageVariants: [UIImage(systemName: "mic.fill")!],
            handler: { [weak self] _ in
                // Trigger voice input
                self?.startListening()
            }
        )
        
        voice.leadingButtonVariants = [button]
        
        voice.tabImage = UIImage(systemName: "mic.fill")
        
        return voice
    }
    
    // MARK: - Music Template
    
    private func createMusicTemplate() -> CPTemplate {
        // Tab bar for music
        let music = CPTabBarTemplate(templates: [
            createNowPlayingTemplate(),
            createMusicSearchTemplate()
        ])
        
        music.tabImage = UIImage(systemName: "music.note.list")
        
        return music
    }
    
    private func createNowPlayingTemplate() -> CPTemplate {
        let nowPlaying = CPNowPlayingTemplate.shared
        nowPlaying.isUpNextButtonEnabled = true
        nowPlaying.isAlbumArtistButtonEnabled = true
        nowPlaying.isPlayPauseButtonEnabled = true
        nowPlaying.isSkipButtonEnabled = true
        
        // Custom transport controls
        nowPlaying.updateNowPlayingButtons([
            createTransportButton(image: "backward.fill", action: "previous"),
            createTransportButton(image: "play.fill", action: "play"),
            createTransportButton(image: "forward.fill", action: "next")
        ])
        
        return nowPlaying
    }
    
    private func createNowPlayingButtons() -> [CPNowPlayingButton] {
        return [
            CPNowPlayingButton(buttonType: .previousTrack) { [weak self] _ in
                self?.voiceCommandHandler?("上一首")
            },
            CPNowPlayingButton(buttonType: .playPause) { [weak self] _ in
                self?.voiceCommandHandler?("播放暫停")
            },
            CPNowPlayingButton(buttonType: .nextTrack) { [weak self] _ in
                self?.voiceCommandHandler?("下一首")
            }
        ]
    }
    
    private func createTransportButton(image: String, action: String) -> CPNowPlayingButton {
        return CPNowPlayingImageButton(image: UIImage(systemName: image)!) { [weak self] _ in
            self?.voiceCommandHandler?(action)
        }
    }
    
    private func createMusicSearchTemplate() -> CPTemplate {
        let search = CPSearchTemplate()
        search.placeholderText = "搜尋歌曲..."
        search.tabImage = UIImage(systemName: "magnifyingglass")
        
        return search
    }
    
    // MARK: - Tasks Template
    
    private func createTasksTemplate() -> CPTemplate {
        let list = CPListTemplate(
            title: "任務",
            sections: [
                CPListSection(
                    items: [
                        CPListItem(title: "我的任務", detailText: "查看所有任務"),
                        CPListItem(title: "新增任務", detailText: "用語音建立"),
                        CPListItem(title: "今天進度", detailText: "工作狀態")
                    ]
                )
            ]
        )
        
        list.tabImage = UIImage(systemName: "checklist")
        
        return list
    }
    
    // MARK: - Navigation Actions
    
    private func switchToVoice() {
        interfaceController?.selectTemplate(atIndex: 1, animated: true)
    }
    
    private func switchToMusic() {
        interfaceController?.selectTemplate(atIndex: 2, animated: true)
    }
    
    private func switchToTasks() {
        interfaceController?.selectTemplate(atIndex: 3, animated: true)
    }
    
    private func showSchedule() {
        // Show schedule information
    }
    
    private func startListening() {
        // Start voice recognition
        voiceCommandHandler?("開始聆聽")
    }
}

// MARK: - Notification Names

extension Notification.Name {
    static let carPlayConnected = Notification.Name("carPlayConnected")
    static let carPlayDisconnected = Notification.Name("carPlayDisconnected")
}

// MARK: - CarPlay Connection Manager

class CarPlayManager: ObservableObject {
    @Published var isConnected = false
    @Published var isListening = false
    
    init() {
        setupNotifications()
    }
    
    private func setupNotifications() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleConnected),
            name: .carPlayConnected,
            object: nil
        )
        
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleDisconnected),
            name: .carPlayDisconnected,
            object: nil
        )
    }
    
    @objc private func handleConnected() {
        DispatchQueue.main.async {
            self.isConnected = true
            // Auto-start listening when connected
            self.isListening = true
        }
    }
    
    @objc private func handleDisconnected() {
        DispatchQueue.main.async {
            self.isConnected = false
            self.isListening = false
        }
    }
    
    deinit {
        NotificationCenter.default.removeObserver(self)
    }
}
