const { useState, useEffect, useRef } = React;

const VoiceOrb = ({ 
  isConnected, 
  isListening, 
  isProcessing, 
  audioLevel = 0, 
  onToggleVoice 
}) => {
  const [particles, setParticles] = useState([]);
  const [animationTime, setAnimationTime] = useState(0);
  const containerRef = useRef(null);
  const animationFrameRef = useRef(null);

  // Generate particles in a 3D sphere formation
  useEffect(() => {
    const generateParticles = () => {
      // Reduced particle count for smooth animation
      const particleCount = window.innerWidth <= 768 ? 150 : 300;
      const newParticles = [];
      
      for (let i = 0; i < particleCount; i++) {
        // Generate spherical coordinates
        const phi = Math.acos(1 - 2 * Math.random()); // 0 to π
        const theta = 2 * Math.PI * Math.random(); // 0 to 2π
        const radius = 180 + Math.random() * 40; // Varying radius for depth
        
        // Convert to Cartesian coordinates
        const x = radius * Math.sin(phi) * Math.cos(theta);
        const y = radius * Math.sin(phi) * Math.sin(theta);
        const z = radius * Math.cos(phi);
        
        // Create color gradient based on y position (height)
        const normalizedY = (y + radius) / (2 * radius); // 0 to 1
        const hue = 240 - (normalizedY * 180); // Blue (240) to Red (60)
        const saturation = 70 + (normalizedY * 30); // 70% to 100%
        const lightness = 50 + (normalizedY * 30); // 50% to 80%
        
        newParticles.push({
          id: i,
          originalX: x,
          originalY: y,
          originalZ: z,
          x: x,
          y: y,
          z: z,
          size: 2 + Math.random() * 3, // Larger particles to compensate for fewer count
          opacity: 0.5 + Math.random() * 0.5,
          color: `hsl(${Math.round(hue)}, ${Math.round(saturation)}%, ${Math.round(lightness)}%)`,
          phase: Math.random() * Math.PI * 2,
          speed: 0.3 + Math.random() * 0.7 // Slower movement for smoother animation
        });
      }
      
      setParticles(newParticles);
    };

    generateParticles();
  }, []);

  // Optimized animation loop using useRef for smooth 60fps
  useEffect(() => {
    let lastTime = 0;
    const frameRate = 1000 / 60; // 60fps
    
    const animate = (currentTime) => {
      // Throttle to 60fps
      if (currentTime - lastTime < frameRate) {
        animationFrameRef.current = requestAnimationFrame(animate);
        return;
      }
      lastTime = currentTime;
      
      const time = currentTime * 0.001;
      setAnimationTime(time);
      
      // Audio reactivity - calculate once per frame
      let reactiveScale = 1;
      if (isListening) {
        reactiveScale = 1 + audioLevel * 0.3;
      } else if (isProcessing) {
        reactiveScale = 1 + Math.sin(time * 2) * 0.05;
      } else if (isConnected) {
        reactiveScale = 1 + Math.sin(time * 0.5) * 0.02;
      }
      
      // Update particles with optimized calculations
      setParticles(prevParticles => {
        if (prevParticles.length === 0) return prevParticles;
        
        return prevParticles.map(particle => {
          // Simplified floating animation
          const timeOffset = time * particle.speed + particle.phase;
          const floatX = particle.originalX + Math.sin(timeOffset) * 3;
          const floatY = particle.originalY + Math.cos(timeOffset * 1.1) * 3;
          const floatZ = particle.originalZ + Math.sin(timeOffset * 0.8) * 3;
          
          return {
            ...particle,
            x: floatX * reactiveScale,
            y: floatY * reactiveScale,
            z: floatZ * reactiveScale
          };
        });
      });
      
      animationFrameRef.current = requestAnimationFrame(animate);
    };
    
    animationFrameRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isListening, isProcessing, isConnected, audioLevel]);

  const getParticleStyle = (particle) => {
    // Project 3D coordinates to 2D
    const perspective = 1000;
    const scale = perspective / (perspective + particle.z);
    const x2d = particle.x * scale;
    const y2d = particle.y * scale;
    
    // Calculate opacity based on z-depth
    const depthOpacity = Math.max(0.1, Math.min(1, (particle.z + 220) / 440));
    const finalOpacity = particle.opacity * depthOpacity;
    
    // Size based on depth and audio
    let finalSize = particle.size * scale;
    if (isListening) {
      finalSize *= (1 + audioLevel * 0.5);
    }
    
    return {
      position: 'absolute',
      left: '50%',
      top: '50%',
      width: `${finalSize}px`,
      height: `${finalSize}px`,
      backgroundColor: particle.color,
      borderRadius: '50%',
      transform: `translate(${x2d}px, ${y2d}px)`,
      opacity: finalOpacity,
      boxShadow: `0 0 ${finalSize * 2}px ${particle.color}`,
      pointerEvents: 'none'
    };
  };

  return (
    <div className="voice-orb-container" onClick={onToggleVoice}>
      <div 
        ref={containerRef}
        className="particle-sphere"
        style={{
          position: 'relative',
          width: '600px',
          height: '600px',
          cursor: 'pointer'
        }}
      >
        {particles.map(particle => (
          <div
            key={particle.id}
            className="sphere-particle"
            style={getParticleStyle(particle)}
          />
        ))}
      </div>
    </div>
  );
};

window.VoiceOrb = VoiceOrb;