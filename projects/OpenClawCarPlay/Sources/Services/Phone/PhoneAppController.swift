import UIKit
import Intents

class PhoneAppController: ObservableObject {
    @Published var isAuthorized = false
    
    // MARK: - Authorization
    
    func requestSiriAuthorization() {
        INPreferences.requestSiriAuthorization { status in
            DispatchQueue.main.async {
                switch status {
                case .authorized:
                    self.isAuthorized = true
                    print("Siri authorized")
                case .denied, .restricted, .notDetermined:
                    self.isAuthorized = false
                    print("Siri not authorized: \(status)")
                @unknown default:
                    break
                }
            }
        }
    }
    
    // MARK: - Open Apps
    
    func openApp(bundleID: String) -> Bool {
        guard let url = URL(string: bundleID) else { return false }
        
        if UIApplication.shared.canOpenURL(url) {
            UIApplication.shared.open(url, options: [:], completionHandler: nil)
            return true
        }
        return false
    }
    
    // Common app bundle IDs
    struct AppBundleIDs {
        static let phone = "com.apple.mobilephone"
        static let messages = "com.apple.MobileSMS"
        static let music = "com.apple.Music"
        static let maps = "com.apple.Maps"
        static let calendar = "com.apple.mobilecal"
        static let notes = "com.apple.mobilenotes"
        static let reminders = "com.apple.reminders"
        static let settings = "com.apple.Preferences"
        static let safari = "com.apple.mobilesafari"
        static let podcasts = "com.apple.podcasts"
    }
    
    // MARK: - Quick Actions
    
    func makeCall(to number: String) {
        guard let url = URL(string: "tel://\(number.replacingOccurrences(of: " ", with: ""))") else { return }
        UIApplication.shared.open(url)
    }
    
    func sendMessage(to contact: String, message: String) {
        // Use SMS intent or open Messages app
        if let url = URL(string: "sms:\(contact)") {
            UIApplication.shared.open(url)
        }
    }
    
    func setAlarm(time: Date, label: String = "OpenClaw") {
        // Open Clock app with alarm
        if let url = URL(string: "clock://alarm") {
            UIApplication.shared.open(url)
        }
    }
    
    func createReminder(title: String, date: Date) {
        // Open Reminders app
        if let url = URL(string: "reminders://") {
            UIApplication.shared.open(url)
        }
    }
    
    // MARK: - Intents (Siri)
    
    func donateShortcut(_ phrase: String) {
        let activity = NSUserActivity(activityType: "com.openclaw.carplay.\(phrase)")
        activity.title = phrase
        activity.isEligibleForSearch = true
        activity.isEligibleForPrediction = true
        activity.suggestedInvocationPhrase = phrase
        activity.becomeCurrent()
    }
}

// MARK: - App Control Commands

extension PhoneAppController {
    
    func handleCommand(_ command: String) -> String {
        let lowercased = command.lowercased()
        
        if lowercased.contains("打電話") || lowercased.contains("call") {
            // Extract phone number
            return "正在打開電話..."
        }
        
        if lowercased.contains("訊息") || lowercased.contains("message") {
            openApp(bundleID: AppBundleIDs.messages)
            return "正在打開訊息..."
        }
        
        if lowercased.contains("音樂") || lowercased.contains("music") {
            openApp(bundleID: AppBundleIDs.music)
            return "正在打開音樂..."
        }
        
        if lowercased.contains("地圖") || lowercased.contains("map") {
            openApp(bundleID: AppBundleIDs.maps)
            return "正在打開地圖..."
        }
        
        if lowercased.contains("日曆") || lowercased.contains("calendar") {
            openApp(bundleID: AppBundleIDs.calendar)
            return "正在打開日曆..."
        }
        
        if lowercased.contains("提醒") || lowercased.contains("reminder") {
            openApp(bundleID: AppBundleIDs.reminders)
            return "正在打開提醒事項..."
        }
        
        if lowercased.contains("筆記") || lowercased.contains("note") {
            openApp(bundleID: AppBundleIDs.notes)
            return "正在打開筆記..."
        }
        
        if lowercased.contains("設定") || lowercased.contains("setting") {
            openApp(bundleID: AppBundleIDs.settings)
            return "正在打開設定..."
        }
        
        if lowercased.contains("瀏覽器") || lowercased.contains("safari") {
            openApp(bundleID: AppBundleIDs.safari)
            return "正在打開Safari..."
        }
        
        if lowercased.contains("播客") || lowercased.contains("podcast") {
            openApp(bundleID: AppBundleIDs.podcasts)
            return "正在打開播客..."
        }
        
        return "無法識別指令"
    }
}
