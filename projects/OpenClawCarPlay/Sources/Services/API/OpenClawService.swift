import Foundation

class OpenClawService: ObservableObject {
    @Published var isConnected = false
    @Published var lastResponse: String?
    @Published var errorMessage: String?
    
    // OpenClaw API Configuration
    private let baseURL = "http://localhost:8080/api"
    private let userID = "carplay-ios"
    
    init() {
        checkConnection()
    }
    
    // MARK: - Connection
    
    func checkConnection() {
        // Ping OpenClaw gateway
        guard let url = URL(string: "\(baseURL)/ping") else { return }
        
        URLSession.shared.dataTask(with: url) { [weak self] _, response, error in
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
        guard let url = URL(string: "\(baseURL)/voice") else { return }
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            urlRequest.httpBody = try JSONEncoder().encode(request)
        } catch {
            errorMessage = "Encoding error"
            return
        }
        
        URLSession.shared.dataTask(with: urlRequest) { data, response, error in
            // For demo, simulate response
            DispatchQueue.main.async {
                let mockResponse = OpenClawResponse(
                    success: true,
                    message: "收到指令：\(request.text)",
                    data: nil
                )
                completion(mockResponse)
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
