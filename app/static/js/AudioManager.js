class AudioManager {
  constructor() {
    this.websocket = null;
    this.sessionId = Math.random().toString().substring(10);
    this.isAudio = false;
    this.currentMessageId = null;
    this.isRecording = false;
    this.intentionalClose = false; // Flag to prevent auto-reconnect
    
    // Audio components
    this.audioPlayerNode = null;
    this.audioPlayerContext = null;
    this.audioRecorderNode = null;
    this.audioRecorderContext = null;
    this.micStream = null;
    this.analyzerNode = null;
    this.frequencyData = null;
    
    // Event callbacks
    this.onConnectionChange = null;
    this.onMessage = null;
    this.onAudioLevel = null;
    this.onRecordingChange = null;
    this.onProcessingChange = null;
    
    this.audioLevel = 0;
    this.isProcessing = false;
    
    // Audio debugging stats
    this.audioChunksSent = 0;
    this.totalAudioBytesSent = 0;
    this.audioStartTime = null;
  }

  // Initialize the audio manager
  async init() {
    await this.connectWebSocket();
  }

  // Connect to WebSocket
  async connectWebSocket() {
    // Close existing connection if any
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }

    const wsUrl = `ws://${window.location.host}/ws/${this.sessionId}?is_audio=${this.isAudio}`;
    console.log("Connecting to:", wsUrl);
    
    return new Promise((resolve, reject) => {
      this.websocket = new WebSocket(wsUrl);

      this.websocket.onopen = () => {
        console.log("WebSocket connection opened with audio mode:", this.isAudio);
        this.onConnectionChange?.(true);
        resolve();
      };

      this.websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log("[AGENT TO CLIENT]", message);
        this.handleIncomingMessage(message);
      };

      this.websocket.onclose = (event) => {
        console.log("WebSocket connection closed. Code:", event.code, "Reason:", event.reason);
        this.onConnectionChange?.(false);
        
        // Only auto-reconnect if it wasn't an intentional close
        if (!this.intentionalClose) {
          setTimeout(() => {
            console.log("Reconnecting...");
            this.connectWebSocket();
          }, 5000);
        } else {
          // Reset the flag after intentional close
          this.intentionalClose = false;
        }
      };

      this.websocket.onerror = (e) => {
        console.log("WebSocket error:", e);
        this.onConnectionChange?.(false);
        reject(e);
      };
    });
  }

  // Handle incoming messages from the agent
  handleIncomingMessage(message) {
    console.log("Handling message:", message);
    
    // Handle turn completion
    if (message.turn_complete) {
      this.currentMessageId = null;
      this.isProcessing = false;
      this.onProcessingChange?.(false);
      return;
    }

    // Start processing indication for first message
    if (!message.turn_complete && 
        (message.mime_type === "text/plain" || message.mime_type === "audio/pcm")) {
      this.isProcessing = true;
      this.onProcessingChange?.(true);
    }

    // Handle audio playback
    if (message.mime_type === "audio/pcm" && this.audioPlayerNode) {
      const audioData = this.base64ToArray(message.data);
      this.audioPlayerNode.port.postMessage(audioData);
    }

    // Handle text messages
    if (message.mime_type === "text/plain") {
      this.onMessage?.(message);
    }
  }

  // Start audio recording and analysis
  async startAudio() {
    try {
      console.log("Starting audio...");
      
      // Reset debugging stats
      this.audioChunksSent = 0;
      this.totalAudioBytesSent = 0;
      this.audioStartTime = Date.now();
      
      // Set audio mode first
      this.isAudio = true;
      this.isRecording = true;
      this.onRecordingChange?.(true);

      // Reconnect WebSocket with audio mode
      await this.connectWebSocket();

      // Start audio worklets
      await this.initializeAudioWorklets();

      console.log("Audio started successfully");
    } catch (error) {
      console.error("Error starting audio:", error);
      this.isRecording = false;
      this.isAudio = false;
      this.onRecordingChange?.(false);
    }
  }

  async initializeAudioWorklets() {
    try {
      // Start audio output
      const audioPlayerSetup = await this.startAudioPlayerWorklet();
      this.audioPlayerNode = audioPlayerSetup[0];
      this.audioPlayerContext = audioPlayerSetup[1];

      // Start audio input with analysis
      const audioRecorderSetup = await this.startAudioRecorderWorklet();
      this.audioRecorderNode = audioRecorderSetup[0];
      this.audioRecorderContext = audioRecorderSetup[1];
      this.micStream = audioRecorderSetup[2];

      // Set up frequency analysis
      this.analyzerNode = this.audioRecorderContext.createAnalyser();
      this.analyzerNode.fftSize = 256;
      this.frequencyData = new Uint8Array(this.analyzerNode.frequencyBinCount);

      // Connect analyzer
      const source = this.audioRecorderContext.createMediaStreamSource(this.micStream);
      source.connect(this.analyzerNode);

      // Start frequency analysis loop
      this.startFrequencyAnalysis();
    } catch (error) {
      console.error("Error initializing audio worklets:", error);
      throw error;
    }
  }

  // Stop audio recording
  async stopAudio() {
    console.log("Stopping audio...");
    
    if (this.audioRecorderNode) {
      this.audioRecorderNode.disconnect();
      this.audioRecorderNode = null;
    }

    if (this.audioRecorderContext) {
      this.audioRecorderContext.close().catch(err => 
        console.error("Error closing audio context:", err)
      );
      this.audioRecorderContext = null;
    }

    if (this.micStream) {
      this.micStream.getTracks().forEach(track => track.stop());
      this.micStream = null;
    }

    this.isRecording = false;
    this.isAudio = false;
    this.audioLevel = 0;
    this.onRecordingChange?.(false);
    this.onAudioLevel?.(0);

    // Reconnect without audio mode
    await this.connectWebSocket();
  }

  // Analyze audio frequency for visualization
  startFrequencyAnalysis() {
    const analyze = () => {
      if (!this.isRecording || !this.analyzerNode) return;

      this.analyzerNode.getByteFrequencyData(this.frequencyData);
      
      // Calculate average volume level
      let sum = 0;
      for (let i = 0; i < this.frequencyData.length; i++) {
        sum += this.frequencyData[i];
      }
      this.audioLevel = (sum / this.frequencyData.length) / 255;
      
      this.onAudioLevel?.(this.audioLevel);
      requestAnimationFrame(analyze);
    };
    
    analyze();
  }

  // Send message to the agent
  sendMessage(message) {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      // Enhanced logging for audio messages
      if (message.mime_type === "audio/pcm") {
        this.audioChunksSent++;
        const audioBytes = this.base64ToArray(message.data);
        this.totalAudioBytesSent += audioBytes.byteLength;
        
        const elapsedTime = Date.now() - this.audioStartTime;
        const bytesPerSecond = this.totalAudioBytesSent / (elapsedTime / 1000);
        const expectedRate = 24000 * 2; // 24kHz * 2 bytes per sample (matches AudioContext sample rate)
        
        console.log(`[CLIENT TO AGENT] Audio chunk #${this.audioChunksSent}:`);
        console.log(`  - Chunk size: ${audioBytes.byteLength} bytes`);
        console.log(`  - Base64 size: ${message.data.length} chars`);
        console.log(`  - Total sent: ${this.totalAudioBytesSent} bytes`);
        console.log(`  - Elapsed time: ${elapsedTime} ms`);
        console.log(`  - Current rate: ${bytesPerSecond.toFixed(0)} bytes/sec`);
        console.log(`  - Expected rate: ${expectedRate} bytes/sec`);
        console.log(`  - Rate ratio: ${(bytesPerSecond / expectedRate).toFixed(2)}x`);
        
        // Show first few bytes as hex for debugging
        const firstBytes = new Uint8Array(audioBytes.slice(0, 16));
        const hexString = Array.from(firstBytes).map(b => b.toString(16).padStart(2, '0')).join(' ');
        console.log(`  - First 16 bytes: ${hexString}`);
        
        // Calculate approximate audio duration
        const sampleCount = audioBytes.byteLength / 2; // 16-bit samples
        const durationMs = (sampleCount / 24000) * 1000; // 24kHz sample rate
        console.log(`  - Audio duration: ${durationMs.toFixed(2)} ms`);
      }
      
      this.websocket.send(JSON.stringify(message));
    }
  }

  // Send text message
  sendTextMessage(text) {
    this.sendMessage({
      mime_type: "text/plain",
      data: text,
      role: "user"
    });
  }

  // Audio worklet setup - use existing audio modules
  async startAudioPlayerWorklet() {
    try {
      // Import and use the existing audio player module
      const { startAudioPlayerWorklet } = await import('./audio-player.js');
      return await startAudioPlayerWorklet();
    } catch (error) {
      console.warn("Could not load audio-player.js, using fallback");
      // Fallback implementation
      const audioContext = new AudioContext({ sampleRate: 24000 });
      await audioContext.audioWorklet.addModule('/static/js/pcm-player-processor.js');
      const node = new AudioWorkletNode(audioContext, 'pcm-player-processor');
      node.connect(audioContext.destination);
      return [node, audioContext];
    }
  }

  async startAudioRecorderWorklet() {
    try {
      // Import and use the existing audio recorder module
      const { startAudioRecorderWorklet } = await import('./audio-recorder.js');
      return await startAudioRecorderWorklet((pcmData) => {
        // Handle audio data from the recorder
        if (this.isRecording) {
          this.sendMessage({
            mime_type: "audio/pcm",
            data: this.arrayBufferToBase64(pcmData)
          });
        }
      });
    } catch (error) {
      console.warn("Could not load audio-recorder.js, using fallback");
      // Fallback implementation
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: { 
          sampleRate: 24000,
          channelCount: 1 
        } 
      });
      
      const audioContext = new AudioContext({ sampleRate: 24000 });
      await audioContext.audioWorklet.addModule('/static/js/pcm-recorder-processor.js');
      
      const source = audioContext.createMediaStreamSource(stream);
      const node = new AudioWorkletNode(audioContext, 'pcm-recorder-processor');
      
      source.connect(node);
      
      // Handle audio data from the worklet
      node.port.onmessage = (event) => {
        if (this.isRecording) {
          this.sendMessage({
            mime_type: "audio/pcm",
            data: this.arrayBufferToBase64(event.data)
          });
        }
      };
      
      return [node, audioContext, stream];
    }
  }

  // Utility functions
  base64ToArray(base64) {
    const binaryString = window.atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
  }

  arrayBufferToBase64(buffer) {
    let binary = "";
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
  }
}

window.AudioManager = AudioManager;