import SwiftUI

struct ContentView: View {
    @StateObject private var voiceManager = VoiceManager()
    @StateObject private var openClawService = OpenClawService()
    @State private var isListening = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Status Card
                StatusCard(isConnected: openClawService.isConnected)
                
                // Voice Button
                VoiceButton(isListening: $isListening) {
                    if isListening {
                        voiceManager.stopListening()
                    } else {
                        voiceManager.startListening()
                    }
                }
                
                // Transcript
                if let transcript = voiceManager.transcript {
                    TranscriptView(text: transcript)
                }
                
                // Response
                if let response = openClawService.lastResponse {
                    ResponseView(text: response)
                }
                
                Spacer()
                
                // Quick Actions
                QuickActionsGrid(voiceManager: voiceManager, openClawService: openClawService)
            }
            .padding()
            .navigationTitle("OpenClaw CarPlay")
            .onChange(of: voiceManager.transcript) { newValue in
                if let text = newValue, !text.isEmpty {
                    openClawService.sendMessage(text)
                }
            }
        }
    }
}

struct StatusCard: View {
    let isConnected: Bool
    
    var body: some View {
        HStack {
            Image(systemName: isConnected ? "wifi" : "wifi.slash")
                .foregroundColor(isConnected ? .green : .red)
            Text(isConnected ? "已連接 OpenClaw" : "未連接")
                .font(.headline)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

struct VoiceButton: View {
    @Binding var isListening: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            ZStack {
                Circle()
                    .fill(isListening ? Color.red : Color.blue)
                    .frame(width: 120, height: 120)
                
                Image(systemName: isListening ? "mic.fill" : "mic")
                    .font(.system(size: 50))
                    .foregroundColor(.white)
            }
        }
    }
}

struct TranscriptView: View {
    let text: String
    
    var body: some View {
        Text(text)
            .font(.body)
            .padding()
            .frame(maxWidth: .infinity)
            .background(Color(.systemGray5))
            .cornerRadius(8)
    }
}

struct ResponseView: View {
    let text: String
    
    var body: some View {
        Text(text)
            .font(.body)
            .padding()
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(Color.blue.opacity(0.1))
            .cornerRadius(8)
    }
}

struct QuickActionsGrid: View {
    @ObservedObject var voiceManager: VoiceManager
    @ObservedObject var openClawService: OpenClawService
    
    let columns = [
        GridItem(.flexible()),
        GridItem(.flexible())
    ]
    
    var body: some View {
        LazyVGrid(columns: columns, spacing: 12) {
            QuickActionButton(icon: "magnifyingglass", title: "搜尋") {
                openClawService.search(query: "天氣")
            }
            
            QuickActionButton(icon: "music.note", title: "播放音樂") {
                openClawService.playMusic()
            }
            
            QuickActionButton(icon: "plus.circle", title: "新增任務") {
                openClawService.createTask(title: "測試任務")
            }
            
            QuickActionButton(icon: "calendar", title: "查詢日程") {
                openClawService.getSchedule()
            }
        }
    }
}

struct QuickActionButton: View {
    let icon: String
    let title: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack {
                Image(systemName: icon)
                    .font(.title2)
                Text(title)
                    .font(.caption)
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color(.systemGray5))
            .cornerRadius(12)
        }
    }
}

#Preview {
    ContentView()
}
