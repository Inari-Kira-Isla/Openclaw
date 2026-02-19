import AVFoundation

class TTSManager: NSObject, ObservableObject {
    @Published var isSpeaking = false
    @Published var speechRate: Float = 0.5 // 0.0 - 1.0
    
    private let synthesizer = AVSpeechSynthesizer()
    private var completionHandler: (() -> Void)?
    
    override init() {
        super.init()
        synthesizer.delegate = self
        configureAudioSession()
    }
    
    // MARK: - Audio Session
    
    private func configureAudioSession() {
        do {
            let audioSession = AVAudioSession.sharedInstance()
            try audioSession.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers, .interruptSpokenAudioAndMixWithOthers])
            try audioSession.setActive(true)
        } catch {
            print("TTS: Audio session error: \(error)")
        }
    }
    
    // MARK: - Speak
    
    func speak(_ text: String, completion: (() -> Void)? = nil) {
        // Stop any current speech
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        
        completionHandler = completion
        
        let utterance = AVSpeechUtterance(string: text)
        
        // Configure voice
        utterance.voice = AVSpeechSynthesisVoice(language: "zh-TW") // Traditional Chinese
        utterance.rate = speechRate
        utterance.pitchMultiplier = 1.0
        utterance.volume = 1.0
        
        // Pre-speech delay
        utterance.preUtteranceDelay = 0.1
        utterance.postUtteranceDelay = 0.1
        
        isSpeaking = true
        synthesizer.speak(utterance)
    }
    
    func speakEnglish(_ text: String, completion: (() -> Void)? = nil) {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        
        completionHandler = completion
        
        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: "en-US")
        utterance.rate = speechRate
        
        isSpeaking = true
        synthesizer.speak(utterance)
    }
    
    // MARK: - Control
    
    func stop() {
        synthesizer.stopSpeaking(at: .immediate)
        isSpeaking = false
    }
    
    func pause() {
        synthesizer.pauseSpeaking(at: .word)
    }
    
    func resume() {
        synthesizer.continueSpeaking()
    }
    
    // MARK: - Settings
    
    func setRate(_ rate: Float) {
        // Rate: 0.0 (slow) - 1.0 (fast)
        speechRate = max(0.1, min(1.0, rate))
    }
    
    // MARK: - Available Voices
    
    func listAvailableVoices() {
        let voices = AVSpeechSynthesisVoice.speechVoices()
        let chineseVoices = voices.filter { $0.language.contains("zh") }
        
        print("Available Chinese voices:")
        for voice in chineseVoices {
            print("  - \(voice.name) (\(voice.language))")
        }
    }
}

// MARK: - AVSpeechSynthesizerDelegate

extension TTSManager: AVSpeechSynthesizerDelegate {
    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didStart utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = true
        }
    }
    
    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.completionHandler?()
            self.completionHandler = nil
        }
    }
    
    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.completionHandler = nil
        }
    }
}

// MARK: - Convenience Extensions

extension TTSManager {
    func speakWeather(_ weather: String) {
        speak("今天\(weather)")
    }
    
    func speakTaskCount(_ count: Int) {
        speak("您有 \(count) 個任務")
    }
    
    func speakSchedule(_ events: [String]) {
        let text = "今天的行程有：" + events.joined(separator: "，")
        speak(text)
    }
    
    func speakMusicPlaying(_ song: String, artist: String) {
        speak("正在播放 \(song)，由 \(artist) 演唱")
    }
}
