import { useEffect, useState, useRef } from 'react';

interface CatMascotProps {
  filledCount: number; // Number of selections made (0-5 for dimensions, up to 7+ with archetypes)
  maxCount?: number;
}



export function CatMascot({ filledCount, maxCount = 7 }: CatMascotProps) {
  const [scrollY, setScrollY] = useState(0);
  const [isVisible, setIsVisible] = useState(true);
  const catRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Cat's vertical position follows scroll with smooth offset
  // Minimum top position keeps cat below the hero section (around 400px from top)
  const minTop = 500;
  const catY = Math.max(minTop, Math.min(scrollY * 0.3 + 100, window.innerHeight - 200));
  
  // Cat expressions based on how full the bowl is
  const getCatFace = () => {
    if (filledCount === 0) return '😺'; // Hopeful
    if (filledCount <= 2) return '😸'; // Happy
    if (filledCount <= 4) return '😻'; // Love
    return '🤩'; // Ecstatic
  };

  // Bowl fill level - fills completely by 5 selections (all taste dimensions)
  const fillPercentage = Math.min((filledCount / 5) * 100, 100);

  return (
    <div
      ref={catRef}
      className="fixed right-4 lg:right-8 z-40 transition-all duration-700 ease-out pointer-events-none hidden md:block"
      style={{ 
        top: `${catY}px`,
        opacity: isVisible ? 1 : 0,
      }}
    >
      <div className="relative animate-fade-in">
        {/* Speech Bubble */}
        <div 
          className={`
            absolute -top-16 -left-4 bg-card border border-border rounded-xl px-3 py-2 shadow-lg
            transition-all duration-500 ease-out
            ${filledCount > 0 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2'}
          `}
        >
          <p className="text-xs font-medium text-foreground whitespace-nowrap">
            {filledCount === 0 && "Feed me choices! 🐱"}
            {filledCount === 1 && "Mmm, more please!"}
            {filledCount === 2 && "Getting yummy!"}
            {filledCount === 3 && "Almost there!"}
            {filledCount === 4 && "So delicious!"}
            {filledCount >= 5 && "Perfect feast! 😻"}
          </p>
          {/* Bubble tail */}
          <div className="absolute -bottom-2 left-6 w-4 h-4 bg-card border-r border-b border-border rotate-45" />
        </div>

        {/* Cat Container */}
        <div className="relative">
          {/* Cat Body */}
          <div 
            className={`
              text-6xl transition-transform duration-300 ease-out
              ${filledCount > 0 ? 'animate-bounce' : ''}
            `}
            style={{ 
              animationDuration: '2s',
              transform: `rotate(${Math.sin(scrollY * 0.01) * 3}deg)`,
            }}
          >
            {getCatFace()}
          </div>

          {/* Bowl with utensils */}
          <div className="relative -mt-4 mx-auto w-16">
            
            {/* Spoon on left */}
            <div className="absolute -left-8 -top-1 text-3xl rotate-[160deg]">🥄</div>
            
            {/* Bowl Container */}
            <div className="relative w-16 h-10 bg-gradient-to-b from-amber-200 to-amber-300 rounded-b-[2rem] rounded-t-lg border-2 border-amber-400 overflow-hidden shadow-lg">
              {/* Green Fill Bar */}
              <div 
                className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-emerald-500 to-emerald-400 transition-all duration-500 ease-out"
                style={{ height: `${fillPercentage}%` }}
              />
              
              {/* Bowl Shine */}
              <div className="absolute top-1 left-2 w-2 h-4 bg-white/30 rounded-full rotate-12" />
            </div>
            
            {/* Hand on right */}
            <div className="absolute -right-8 -top-1 text-3xl">🤚</div>
          </div>
        </div>

      </div>
    </div>
  );
}
