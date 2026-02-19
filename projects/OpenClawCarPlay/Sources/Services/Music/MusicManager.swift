import Foundation
import MediaPlayer

class MusicManager: ObservableObject {
    @Published var isPlaying = false
    @Published var currentTrack: Track?
    @Published var queue: [Track] = []
    
    private let musicPlayer = MPMusicPlayerController.systemMusicPlayer
    
    init() {
        setupNotifications()
    }
    
    // MARK: - Authorization
    
    func requestAuthorization() {
        MPMediaLibrary.requestAuthorization { status in
            DispatchQueue.main.async {
                switch status {
                case .authorized:
                    print("Music library authorized")
                case .denied, .restricted:
                    print("Music library denied/restricted")
                case .notDetermined:
                    print("Music library not determined")
                @unknown default:
                    break
                }
            }
        }
    }
    
    // MARK: - Playback Control
    
    func play() {
        musicPlayer.play()
        isPlaying = true
    }
    
    func pause() {
        musicPlayer.pause()
        isPlaying = false
    }
    
    func togglePlayPause() {
        if isPlaying {
            pause()
        } else {
            play()
        }
    }
    
    func nextTrack() {
        musicPlayer.skipToNextItem()
        updateCurrentTrack()
    }
    
    func previousTrack() {
        musicPlayer.skipToPreviousItem()
        updateCurrentTrack()
    }
    
    func seek(to time: TimeInterval) {
        musicPlayer.currentPlaybackTime = time
    }
    
    // MARK: - Queue Management
    
    func playPlaylist(_ playlistID: String) {
        let query = MPMediaQuery.playlists()
        guard let playlist = query.items?.first(where: { 
            ($0 as? MPMediaPlaylist)?.persistentID.description == playlistID 
        }) as? MPMediaPlaylist else { return }
        
        musicPlayer.setQueue(with: [playlist])
        play()
    }
    
    func searchAndPlay(query: String) {
        let filter = MPMediaPropertyPredicate(
            value: query,
            forProperty: MPMediaItemPropertyTitle,
            comparisonType: .contains
        )
        
        let query = MPMediaQuery.songs()
        query.addFilterPredicate(filter)
        
        guard let items = query.items, !items.isEmpty else { return }
        
        queue = items.map { Track(mediaItem: $0) }
        musicPlayer.setQueue(with: items)
        play()
    }
    
    func addToQueue(_ track: Track) {
        queue.append(track)
    }
    
    // MARK: - Private
    
    private func setupNotifications() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handlePlaybackChanged),
            name: .MPMusicPlayerControllerPlaybackStateDidChange,
            object: musicPlayer
        )
        
        musicPlayer.beginGeneratingPlaybackNotifications()
    }
    
    @objc private func handlePlaybackChanged() {
        isPlaying = musicPlayer.playbackState == .playing
        updateCurrentTrack()
    }
    
    private func updateCurrentTrack() {
        if let item = musicPlayer.nowPlayingItem {
            currentTrack = Track(mediaItem: item)
        }
    }
}

// MARK: - Track Model

struct Track: Identifiable {
    let id: String
    let title: String
    let artist: String
    let album: String
    let duration: TimeInterval
    let artwork: URL?
    
    init(mediaItem: MPMediaItem) {
        self.id = mediaItem.persistentID.description
        self.title = mediaItem.title ?? "Unknown"
        self.artist = mediaItem.artist ?? "Unknown"
        self.album = mediaItem.albumTitle ?? "Unknown"
        self.duration = mediaItem.playbackDuration
        
        if let artworkData = mediaItem.artwork?.image(at: CGSize(width: 300, height: 300))?.pngData() {
            // Save artwork temporarily
            let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("\(id).png")
            try? artworkData.write(to: tempURL)
            self.artwork = tempURL
        } else {
            self.artwork = nil
        }
    }
}
