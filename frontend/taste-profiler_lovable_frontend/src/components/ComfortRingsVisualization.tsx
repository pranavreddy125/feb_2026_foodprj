import { useState, useEffect } from 'react';
import { PersonalityResult } from '@/lib/food-data';
import { User } from 'lucide-react';
import { FoodExplorer } from './FoodExplorer';

interface ComfortRingsVisualizationProps {
  result: PersonalityResult;
}

type RingType = 'core' | 'stretch' | 'experimental' | null;

export function ComfortRingsVisualization({ result }: ComfortRingsVisualizationProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [hoveredRing, setHoveredRing] = useState<RingType>(null);
  const [lockedRing, setLockedRing] = useState<RingType>(null);
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const handleRingHover = (ringId: RingType) => {
    // If a ring is locked, don't respond to hover
    if (lockedRing) return;
    
    if (ringId !== hoveredRing) {
      setIsTransitioning(true);
      setTimeout(() => {
        setHoveredRing(ringId);
        setTimeout(() => setIsTransitioning(false), 150);
      }, 80);
    }
  };

  const handleRingLeave = () => {
    // If a ring is locked, don't respond to hover leave
    if (lockedRing) return;
    
    setIsTransitioning(true);
    setTimeout(() => {
      setHoveredRing(null);
      setTimeout(() => setIsTransitioning(false), 150);
    }, 80);
  };

  const handleRingClick = (ringId: RingType) => {
    if (lockedRing === ringId) {
      // Clicking the same locked ring unlocks it
      setLockedRing(null);
      setHoveredRing(null);
    } else {
      // Lock the new ring
      setLockedRing(ringId);
      setHoveredRing(ringId);
    }
  };

  const ringData = [
    { 
      id: 'experimental' as const, 
      foods: result.comfortRings.ring2, 
      label: 'Experimental',
      description: 'Adventure zone',
      size: 'w-[340px] h-[340px] sm:w-[420px] sm:h-[420px]',
      baseColor: 'border-ring-experimental/40 bg-ring-experimental/5',
      hoverColor: 'border-ring-experimental bg-ring-experimental/25 shadow-[0_0_40px_rgba(239,68,68,0.3)]',
      scale: 'hover:scale-[1.02]',
    },
    { 
      id: 'stretch' as const, 
      foods: result.comfortRings.ring1, 
      label: 'Safe Stretch',
      description: 'Approachable new foods',
      size: 'w-[220px] h-[220px] sm:w-[280px] sm:h-[280px]',
      baseColor: 'border-ring-stretch/50 bg-ring-stretch/8',
      hoverColor: 'border-ring-stretch bg-ring-stretch/30 shadow-[0_0_35px_rgba(59,130,246,0.3)]',
      scale: 'hover:scale-[1.03]',
    },
    { 
      id: 'core' as const, 
      foods: result.comfortRings.ring0, 
      label: 'Core Comfort',
      description: 'Your favorites',
      size: 'w-[140px] h-[140px] sm:w-[180px] sm:h-[180px]',
      baseColor: 'border-ring-core/60 bg-ring-core/10',
      hoverColor: 'border-ring-core bg-ring-core/35 shadow-[0_0_30px_rgba(34,197,94,0.35)]',
      scale: 'hover:scale-[1.05]',
    },
  ];

  const getHoveredFoods = () => {
    if (!hoveredRing) return null;
    const ring = ringData.find(r => r.id === hoveredRing);
    return ring ? { foods: ring.foods, label: ring.label, description: ring.description, id: ring.id } : null;
  };

  const hoveredData = getHoveredFoods();

  return (
    <div className="space-y-8">
      {/* Visual Ring Diagram with Side Panel */}
      <div className="section-card overflow-hidden">
        <h2 className="font-display text-2xl font-bold text-foreground mb-2 text-center">
          Your Comfort Rings
        </h2>
        <p className="text-muted-foreground text-center mb-6">
          {lockedRing ? 'Click the ring again to unlock, or click another ring' : 'Hover over a ring to see foods, click to lock it in place'}
        </p>

        {/* Two Column Layout */}
        <div className="flex flex-col lg:flex-row gap-6 lg:gap-8">
          {/* Left: Concentric Rings */}
          <div className="relative flex items-center justify-center min-h-[320px] sm:min-h-[400px] lg:min-h-[420px] lg:flex-1">
            {ringData.map((ring, ringIndex) => (
              <div
                key={ring.id}
                onMouseEnter={() => handleRingHover(ring.id)}
                onMouseLeave={handleRingLeave}
                onClick={() => handleRingClick(ring.id)}
                className={`
                  absolute rounded-full border-[3px] cursor-pointer
                  transition-all ease-[cubic-bezier(0.34,1.56,0.64,1)]
                  ${ring.size}
                  ${hoveredRing === ring.id ? ring.hoverColor : ring.baseColor}
                  ${hoveredRing === ring.id ? 'scale-[1.03] border-[4px]' : ''}
                  ${lockedRing === ring.id ? 'ring-4 ring-white/50' : ''}
                  ${hoveredRing && hoveredRing !== ring.id ? 'opacity-30 scale-[0.98]' : 'opacity-100'}
                  ${isTransitioning ? 'duration-150' : 'duration-500'}
                  ${isVisible ? 'scale-100' : 'scale-75 opacity-0'}
                `}
                style={{ 
                  transitionDelay: isVisible && !hoveredRing ? '0ms' : `${ringIndex * 30}ms`,
                }}
              />
            ))}
            
            {/* Center - You */}
            <div 
              className={`
                absolute z-10 flex flex-col items-center justify-center
                w-16 h-16 sm:w-20 sm:h-20 rounded-full
                bg-gradient-to-br from-primary to-primary/80
                shadow-lg shadow-primary/30
                transition-all duration-500 delay-500
                ${isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-50'}
                ${hoveredRing ? 'opacity-60' : 'opacity-100'}
              `}
            >
              <User className="w-6 h-6 sm:w-8 sm:h-8 text-primary-foreground" />
              <span className="text-[10px] sm:text-xs font-semibold text-primary-foreground mt-0.5">YOU</span>
            </div>
          </div>

          {/* Right: Info Panel */}
          <div className="lg:w-[320px] lg:flex-shrink-0">
            <div 
              className={`
                h-full min-h-[200px] lg:min-h-[400px] rounded-xl border-2 p-5
                transition-all duration-500 ease-out
                ${hoveredData 
                  ? hoveredData.id === 'core' 
                    ? 'border-ring-core bg-ring-core/5' 
                    : hoveredData.id === 'stretch' 
                      ? 'border-ring-stretch bg-ring-stretch/5' 
                      : 'border-ring-experimental bg-ring-experimental/5'
                  : 'border-border bg-muted/30'
                }
              `}
            >
              {hoveredData ? (
                <div className="animate-fade-in">
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`w-4 h-4 rounded-full ${
                      hoveredData.id === 'core' ? 'bg-ring-core' : 
                      hoveredData.id === 'stretch' ? 'bg-ring-stretch' : 'bg-ring-experimental'
                    }`} />
                    <div>
                      <h4 className="font-display font-bold text-lg text-foreground">{hoveredData.label}</h4>
                      <p className="text-xs text-muted-foreground">{hoveredData.description}</p>
                    </div>
                    <span className={`
                      ml-auto px-2.5 py-1 rounded-full text-xs font-semibold text-white
                      ${hoveredData.id === 'core' ? 'bg-ring-core' : 
                        hoveredData.id === 'stretch' ? 'bg-ring-stretch' : 'bg-ring-experimental'}
                    `}>
                      {hoveredData.foods.length}
                    </span>
                  </div>
                  
                  <div className="flex flex-wrap gap-2">
                    {hoveredData.foods.map((food, index) => (
                      <span
                        key={food.name}
                        className={`
                          px-3 py-1.5 rounded-full text-sm font-medium text-white
                          opacity-0 animate-scale-in shadow-sm
                          ${hoveredData.id === 'core' ? 'bg-ring-core' : 
                            hoveredData.id === 'stretch' ? 'bg-ring-stretch' : 'bg-ring-experimental'}
                        `}
                        style={{ animationDelay: `${index * 40}ms` }}
                      >
                        {food.name}
                      </span>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-center">
                  <div className="w-12 h-12 rounded-full bg-muted/50 flex items-center justify-center mb-3">
                    <div className="w-6 h-6 rounded-full border-2 border-dashed border-muted-foreground/40" />
                  </div>
                  <p className="text-muted-foreground font-medium">Hover over a ring</p>
                  <p className="text-sm text-muted-foreground/70">to see foods in that zone</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap justify-center gap-4 mt-6">
          {[
            { id: 'core' as const, label: 'Core Comfort', color: 'bg-ring-core', count: result.comfortRings.ring0.length },
            { id: 'stretch' as const, label: 'Safe Stretch', color: 'bg-ring-stretch', count: result.comfortRings.ring1.length },
            { id: 'experimental' as const, label: 'Experimental', color: 'bg-ring-experimental', count: result.comfortRings.ring2.length },
          ].map((item, index) => (
            <button 
              key={item.label}
              onMouseEnter={() => handleRingHover(item.id)}
              onMouseLeave={handleRingLeave}
              onClick={() => handleRingClick(item.id)}
              className={`
                flex items-center gap-2 px-3 py-1.5 rounded-full
                cursor-pointer
                ${hoveredRing === item.id ? 'bg-muted scale-105' : 'bg-muted/50 hover:bg-muted/70'}
                ${lockedRing === item.id ? 'ring-2 ring-primary' : ''}
                ${isVisible ? 'opacity-100 translate-y-0 transition-all duration-300' : 'opacity-0 translate-y-4 transition-all duration-300'}
              `}
              style={{ transitionDelay: isVisible ? '0ms' : `${700 + index * 100}ms` }}
            >
              <div className={`w-3 h-3 rounded-full ${item.color}`} />
              <span className="text-sm font-medium text-foreground">{item.label}</span>
              <span className="text-xs text-muted-foreground">({item.count})</span>
            </button>
          ))}
        </div>
      </div>

      {/* Food Explorer */}
      <FoodExplorer 
        ring0={result.comfortRings.ring0}
        ring1={result.comfortRings.ring1}
        ring2={result.comfortRings.ring2}
      />
    </div>
  );
}
