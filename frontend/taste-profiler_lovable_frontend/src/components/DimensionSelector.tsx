import { useState } from 'react';
import { TASTE_DIMENSIONS, TasteDimensionId } from '@/lib/food-data';

interface DimensionSelectorProps {
  dimensionId: TasteDimensionId;
  value: number | null;
  onChange: (value: number) => void;
  error?: string;
}

const DIMENSION_ICONS: Record<string, { icon: string; colors: string[] }> = {
  spice_intensity: { 
    icon: '🌶️', 
    colors: ['bg-green-100 border-green-300 hover:border-green-400', 'bg-orange-100 border-orange-300 hover:border-orange-400', 'bg-red-100 border-red-300 hover:border-red-400']
  },
  texture_intensity: { 
    icon: '🥄', 
    colors: ['bg-blue-50 border-blue-200 hover:border-blue-300', 'bg-purple-50 border-purple-200 hover:border-purple-300', 'bg-pink-50 border-pink-200 hover:border-pink-300']
  },
  preparation_familiarity: { 
    icon: '👨‍🍳', 
    colors: ['bg-amber-50 border-amber-200 hover:border-amber-300', 'bg-yellow-50 border-yellow-200 hover:border-yellow-300', 'bg-lime-50 border-lime-200 hover:border-lime-300']
  },
  richness: { 
    icon: '🧈', 
    colors: ['bg-sky-50 border-sky-200 hover:border-sky-300', 'bg-indigo-50 border-indigo-200 hover:border-indigo-300', 'bg-violet-50 border-violet-200 hover:border-violet-300']
  },
  psychological_distance: { 
    icon: '🌍', 
    colors: ['bg-emerald-50 border-emerald-200 hover:border-emerald-300', 'bg-teal-50 border-teal-200 hover:border-teal-300', 'bg-cyan-50 border-cyan-200 hover:border-cyan-300']
  },
};

const OPTION_EMOJIS: Record<string, string[]> = {
  spice_intensity: ['🥒', '🌶️', '🔥'],
  texture_intensity: ['🍮', '🥗', '🍿'],
  preparation_familiarity: ['🏠', '🍳', '🧪'],
  richness: ['🥬', '🍝', '🧀'],
  psychological_distance: ['🏡', '🗺️', '🚀'],
};

export function DimensionSelector({ dimensionId, value, onChange, error }: DimensionSelectorProps) {
  const [hoveredOption, setHoveredOption] = useState<number | null>(null);
  const dimension = TASTE_DIMENSIONS.find(d => d.id === dimensionId);
  const iconConfig = DIMENSION_ICONS[dimensionId] || { icon: '🍽️', colors: ['bg-muted', 'bg-muted', 'bg-muted'] };
  const optionEmojis = OPTION_EMOJIS[dimensionId] || ['1️⃣', '2️⃣', '3️⃣'];
  
  if (!dimension) return null;

  return (
    <div className="space-y-3 group">
      <div className="flex items-center gap-3">
        <span className="text-2xl group-hover:scale-110 transition-transform duration-300">{iconConfig.icon}</span>
        <div>
          <h3 className="font-semibold text-foreground">{dimension.label}</h3>
          <p className="text-sm text-muted-foreground">{dimension.description}</p>
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-3">
        {dimension.options.map((option, index) => {
          const isSelected = value === option.value;
          const isHovered = hoveredOption === index;
          
          return (
            <button
              key={option.value}
              type="button"
              onClick={() => onChange(option.value)}
              onMouseEnter={() => setHoveredOption(index)}
              onMouseLeave={() => setHoveredOption(null)}
              className={`
                relative py-4 px-3 rounded-xl border-2 text-center
                transition-all duration-300 ease-out
                ${isSelected 
                  ? 'border-primary bg-primary/10 shadow-lg shadow-primary/20 scale-[1.02]' 
                  : iconConfig.colors[index]
                }
                ${isHovered && !isSelected ? 'scale-[1.03] shadow-md' : ''}
                ${error ? 'border-destructive/50' : ''}
              `}
            >
              {/* Emoji indicator */}
              <div 
                className={`
                  text-3xl mb-2 transition-all duration-300
                  ${isSelected ? 'scale-125 animate-bounce' : ''}
                  ${isHovered ? 'scale-110' : ''}
                `}
                style={{ animationDuration: '1s' }}
              >
                {optionEmojis[index]}
              </div>
              
              {/* Label */}
              <div className={`font-bold text-sm ${isSelected ? 'text-primary' : 'text-foreground'}`}>
                {option.label}
              </div>
              
              {/* Description */}
              <div className={`text-xs mt-1 ${isSelected ? 'text-primary/80' : 'text-muted-foreground'}`}>
                {option.description}
              </div>
              
              {/* Selected checkmark */}
              {isSelected && (
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-primary rounded-full flex items-center justify-center shadow-md animate-scale-in">
                  <span className="text-primary-foreground text-xs">✓</span>
                </div>
              )}
              
              {/* Hover glow effect */}
              <div 
                className={`
                  absolute inset-0 rounded-xl bg-gradient-to-t from-primary/5 to-transparent
                  transition-opacity duration-300
                  ${isHovered || isSelected ? 'opacity-100' : 'opacity-0'}
                `} 
              />
            </button>
          );
        })}
      </div>
      
      {error && (
        <p className="text-sm text-destructive flex items-center gap-1">
          <span>⚠️</span> {error}
        </p>
      )}
    </div>
  );
}
