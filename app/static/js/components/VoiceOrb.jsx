const { useState, useEffect, useRef } = React;

const VoiceOrb = ({ 
  isConnected, 
  isListening, 
  isProcessing, 
  audioLevel = 0, 
  onToggleVoice 
}) => {
  const [animationScale, setAnimationScale] = useState(1);
  const orbRef = useRef(null);
  const animationFrameRef = useRef(null);

  // Calculate orb scale based on audio level and state
  useEffect(() => {
    const animate = () => {
      let targetScale = 1;
      
      if (isListening) {
        // Audio reactive scaling when listening
        targetScale = 1 + (audioLevel * 0.5);
      } else if (isProcessing) {
        // Gentle pulsing when processing
        targetScale = 1 + Math.sin(Date.now() * 0.005) * 0.1;
      } else if (isConnected) {
        // Subtle breathing when idle but connected
        targetScale = 1 + Math.sin(Date.now() * 0.002) * 0.05;
      }
      
      // Smooth interpolation
      setAnimationScale(prev => prev + (targetScale - prev) * 0.1);
      
      animationFrameRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isListening, isProcessing, isConnected, audioLevel]);

  const getOrbColor = () => {
    if (!isConnected) return '#666666';
    if (isProcessing) return '#EA4335';
    if (isListening) return '#34A853';
    return '#4285F4';
  };

  const getOrbGlow = () => {
    if (!isConnected) return 'none';
    const color = getOrbColor();
    const intensity = isListening ? audioLevel * 50 + 20 : 20;
    return `0 0 ${intensity}px ${color}, 0 0 ${intensity * 2}px ${color}`;
  };

  return (
    <div className="voice-orb-container">
      <div className="voice-orb-background">
        {/* Animated background particles */}
        {Array.from({ length: 50 }, (_, i) => (
          <div 
            key={i} 
            className="particle" 
            style={{
              '--delay': `${i * 0.1}s`,
              '--random': Math.random()
            }}
          />
        ))}
      </div>
      
      <div 
        ref={orbRef}
        className="voice-orb"
        onClick={onToggleVoice}
        style={{
          transform: `scale(${animationScale})`,
          backgroundColor: getOrbColor(),
          boxShadow: getOrbGlow(),
          cursor: 'pointer'
        }}
      >
        <div className="orb-inner">
          <div className="orb-core" />
          {/* Concentric rings for depth */}
          <div className="orb-ring ring-1" />
          <div className="orb-ring ring-2" />
          <div className="orb-ring ring-3" />
        </div>
        
        {/* Audio visualization bars */}
        {isListening && (
          <div className="audio-visualization">
            {Array.from({ length: 12 }, (_, i) => (
              <div 
                key={i}
                className="audio-bar"
                style={{
                  '--index': i,
                  '--height': `${20 + audioLevel * 60}%`,
                  animationDelay: `${i * 0.1}s`
                }}
              />
            ))}
          </div>
        )}
      </div>
      
      <div className="status-text">
        {!isConnected && "Connecting..."}
        {isConnected && !isListening && !isProcessing && "Click to speak"}
        {isListening && "Listening..."}
        {isProcessing && "Processing..."}
      </div>
    </div>
  );
};

window.VoiceOrb = VoiceOrb;