import Foundation

class OpenClawService: ObservableObject {
    @Published var isConnected = false
    @Published var lastResponse: String?
    @Published var errorMessage: String?
    
    // OpenClaw API Configuration
    private let baseURL = "http://localhost:18789"
    private let userID = "carplay-ios"
    private let token = "openclaw123"
    
    init() {
        checkConnection()
    }
    
    // MARK: - Connection
    
    func checkConnection() {
        // Ping OpenClaw gateway
        guard let url = URL(string: "\(baseURL)/health") else { return }
        
        var urlRequest = URLRequest(url: url)
        urlRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        URLSession.shared.dataTask(with: urlRequest) { [weak self] _, response, error in
            DispatchQueue.main.async {
                if let httpResponse = response as? HTTPURLResponse {
                    self?.isConnected = (httpResponse.statusCode == 200)
                } else {
                    // For demo, simulate connection
                    self?.isConnected = true
                }
            }
        }.resume()
    }
    
    // MARK: - Message
    
    func sendMessage(_ text: String) {
        let request = OpenClawRequest(
            action: "message",
            text: text,
            userID: userID
        )
        
        send(request) { [weak self] response in
            DispatchQueue.main.async {
                self?.lastResponse = response.message
            }
        }
    }
    
    // MARK: - Search
    
    func search(query: String) {
        let request = OpenClawRequest(
            action: "search",
            text: query,
            userID: userID
        )
        
        send(request) { [weak self] response in
            DispatchQueue.main.async {
                self?.lastResponse = response.message
            }
        }
    }
    
    // MARK: - Music
    
    func playMusic() {
        let request = OpenClawRequest(
            action: "music",
            command: "play",
            userID: userID
        )
        
        send(request) { [weak self] response in
            DispatchQueue.main.async {
                self?.lastResponse = response.message
            }
        }
    }
    
    func nextTrack() {
        let request = OpenClawRequest(
            action: "music",
            command: "next",
            userID: userID
        )
        
        send(request) { _ in }
    }
    
    // MARK: - Tasks
    
    func createTask(title: String, description: String = "") {
        let request = OpenClawRequest(
            action: "task",
            command: "create",
            text: title,
            userID: userID
        )
        
        send(request) { [weak self] response in
            DispatchQueue.main.async {
                self?.lastResponse = response.message
            }
        }
    }
    
    func getTasks() {
        let request = OpenClawRequest(
            action: "task",
            command: "list",
            userID: userID
        )
        
        send(request) { [weak self] response in
            DispatchQueue.main.async {
                self?.lastResponse = response.message
            }
        }
    }
    
    // MARK: - Schedule
    
    func getSchedule() {
        let request = OpenClawRequest(
            action: "schedule",
            command: "today",
            userID: userID
        )
        
        send(request) { [weak self] response in
            DispatchQueue.main.async {
                self?.lastResponse = response.message
            }
        }
    }
    
    // MARK: - Private
    
    private func send(_ request: OpenClawRequest, completion: @escaping (OpenClawResponse) -> Void) {
        guard let url = URL(string: "\(baseURL)/v1/responses") else { return }
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        do {
            let body = ["message": request.text ?? request.command ?? ""]
            urlRequest.httpBody = try JSONSerialization.data(withJSONObject: body)
        } catch {
            errorMessage = "Encoding error"
            return
        }
        
        URLSession.shared.dataTask(with: urlRequest) { data, response, error in
            // For demo, simulate response
            DispatchQueue.main.async {
                if let data = data,
                   let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                   let message = json["text"] as? String ?? json["message"] as? String {
                    let mockResponse = OpenClawResponse(
                        success: true,
                        message: message,
                        data: nil
                    )
                    completion(mockResponse)
                } else {
                    let mockResponse = OpenClawResponse(
                        success: true,
                        message: "收到指令：\(request.text ?? request.command ?? "")",
                        data: nil
                    )
                    completion(mockResponse)
                }
            }
        }.resume()
    }
}

// MARK: - Models

struct OpenClawRequest: Codable {
    let action: String
    var text: String?
    var command: String?
    let userID: String
}

struct OpenClawResponse: Codable {
    let success: Bool
    let message: String
    var data: [String: String]?
}
