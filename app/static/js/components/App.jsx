const { useState, useEffect, useRef } = React;

const App = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [messages, setMessages] = useState([]);
  
  const audioManagerRef = useRef(null);

  useEffect(() => {
    console.log("App component mounted");
    
    // Initialize AudioManager
    audioManagerRef.current = new AudioManager();
    
    // Set up event callbacks
    audioManagerRef.current.onConnectionChange = (connected) => {
      console.log("Connection status changed:", connected);
      setIsConnected(connected);
    };
    
    audioManagerRef.current.onRecordingChange = (recording) => {
      console.log("Recording status changed:", recording);
      setIsListening(recording);
    };
    
    audioManagerRef.current.onProcessingChange = (processing) => {
      console.log("Processing status changed:", processing);
      setIsProcessing(processing);
    };
    
    audioManagerRef.current.onAudioLevel = (level) => {
      setAudioLevel(level);
    };
    
    audioManagerRef.current.onMessage = (message) => {
      console.log("Message received:", message);
      setMessages(prev => {
        // Handle streaming messages by updating existing or creating new
        if (message.role === 'model') {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage && lastMessage.role === 'model' && lastMessage.streaming) {
            // Update existing streaming message
            return [
              ...prev.slice(0, -1),
              { ...lastMessage, content: lastMessage.content + message.data }
            ];
          } else {
            // Create new message
            return [
              ...prev,
              { 
                id: Date.now(), 
                role: 'model', 
                content: message.data, 
                streaming: true 
              }
            ];
          }
        }
        return prev;
      });
    };
    
    // Initialize the audio manager
    audioManagerRef.current.init().catch(err => {
      console.error("Failed to initialize AudioManager:", err);
    });
    
    return () => {
      if (audioManagerRef.current) {
        audioManagerRef.current.stopAudio();
      }
    };
  }, []);

  const toggleVoice = async () => {
    if (!audioManagerRef.current) return;
    
    try {
      if (isListening) {
        await audioManagerRef.current.stopAudio();
      } else {
        await audioManagerRef.current.startAudio();
      }
    } catch (error) {
      console.error("Error toggling voice:", error);
    }
  };

  const sendTextMessage = (text) => {
    if (!audioManagerRef.current || !text.trim()) return;
    
    // Add user message to UI
    setMessages(prev => [
      ...prev,
      { id: Date.now(), role: 'user', content: text }
    ]);
    
    // Send to audio manager
    audioManagerRef.current.sendTextMessage(text);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Voice Assistant</h1>
        <p className="subtitle">Powered by Google ADK</p>
      </header>
      
      <main className="app-main">
        <VoiceOrb 
          isConnected={isConnected}
          isListening={isListening}
          isProcessing={isProcessing}
          audioLevel={audioLevel}
          onToggleVoice={toggleVoice}
        />
      </main>
      
      {/* Messages display for debugging/context */}
      {messages.length > 0 && (
        <div className="messages-overlay">
          <div className="messages-container">
            {messages.slice(-3).map(message => (
              <div 
                key={message.id} 
                className={`message ${message.role}`}
              >
                <strong>{message.role}:</strong> {message.content}
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Connection status */}
      <div className="connection-status">
        <div className={`status-dot ${isConnected ? 'connected' : ''}`} />
        <span>
          {isConnected ? 'Connected' : 'Connecting...'}
        </span>
      </div>
    </div>
  );
};

window.App = App;