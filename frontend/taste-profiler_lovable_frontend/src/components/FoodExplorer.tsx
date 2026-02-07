import { useState } from 'react';
import { ComfortFood } from '@/lib/food-data';
import { getFoodMetadata, FoodMetadata } from '@/lib/food-metadata';
import { MapPin, Globe } from 'lucide-react';

interface FoodExplorerProps {
  ring0: ComfortFood[];
  ring1: ComfortFood[];
  ring2: ComfortFood[];
}

export function FoodExplorer({ ring0, ring1, ring2 }: FoodExplorerProps) {
  const [selectedFood, setSelectedFood] = useState<FoodMetadata | null>(null);
  const [selectedRing, setSelectedRing] = useState<'core' | 'stretch' | 'experimental' | null>(null);

  const handleFoodClick = (foodName: string, ring: 'core' | 'stretch' | 'experimental') => {
    const metadata = getFoodMetadata(foodName);
    if (metadata) {
      setSelectedFood(metadata);
      setSelectedRing(ring);
    }
  };

  const ringColors = {
    core: {
      bg: 'bg-ring-core',
      bgLight: 'bg-ring-core/10',
      border: 'border-ring-core',
      text: 'text-ring-core',
    },
    stretch: {
      bg: 'bg-ring-stretch',
      bgLight: 'bg-ring-stretch/10',
      border: 'border-ring-stretch',
      text: 'text-ring-stretch',
    },
    experimental: {
      bg: 'bg-ring-experimental',
      bgLight: 'bg-ring-experimental/10',
      border: 'border-ring-experimental',
      text: 'text-ring-experimental',
    },
  };

  return (
    <div className="section-card">
      <h2 className="font-display text-2xl font-bold text-foreground mb-2 text-center">
        Explore Your Foods
      </h2>
      <p className="text-muted-foreground text-center mb-6">
        Click on any food to learn about its origins and history
      </p>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left: Food List */}
        <div className="lg:w-[280px] flex-shrink-0 space-y-4">
          {/* Core Comfort */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-ring-core" />
              <span className="text-sm font-semibold text-foreground">Core Comfort</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {ring0.map((food, index) => (
                <button
                  key={food.name}
                  onClick={() => handleFoodClick(food.name, 'core')}
                  className={`
                    px-3 py-1.5 rounded-full text-sm font-medium
                    transition-all duration-200 ease-out
                    ${selectedFood?.name === food.name && selectedRing === 'core'
                      ? 'bg-ring-core text-white ring-2 ring-ring-core ring-offset-2 ring-offset-background'
                      : 'bg-ring-core/15 text-ring-core hover:bg-ring-core/25'
                    }
                  `}
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  {food.name}
                </button>
              ))}
            </div>
          </div>

          {/* Safe Stretch */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-ring-stretch" />
              <span className="text-sm font-semibold text-foreground">Safe Stretch</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {ring1.map((food, index) => (
                <button
                  key={food.name}
                  onClick={() => handleFoodClick(food.name, 'stretch')}
                  className={`
                    px-3 py-1.5 rounded-full text-sm font-medium
                    transition-all duration-200 ease-out
                    ${selectedFood?.name === food.name && selectedRing === 'stretch'
                      ? 'bg-ring-stretch text-white ring-2 ring-ring-stretch ring-offset-2 ring-offset-background'
                      : 'bg-ring-stretch/15 text-ring-stretch hover:bg-ring-stretch/25'
                    }
                  `}
                  style={{ animationDelay: `${index * 50 + 100}ms` }}
                >
                  {food.name}
                </button>
              ))}
            </div>
          </div>

          {/* Experimental */}
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-ring-experimental" />
              <span className="text-sm font-semibold text-foreground">Experimental</span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {ring2.map((food, index) => (
                <button
                  key={food.name}
                  onClick={() => handleFoodClick(food.name, 'experimental')}
                  className={`
                    px-3 py-1.5 rounded-full text-sm font-medium
                    transition-all duration-200 ease-out
                    ${selectedFood?.name === food.name && selectedRing === 'experimental'
                      ? 'bg-ring-experimental text-white ring-2 ring-ring-experimental ring-offset-2 ring-offset-background'
                      : 'bg-ring-experimental/15 text-ring-experimental hover:bg-ring-experimental/25'
                    }
                  `}
                  style={{ animationDelay: `${index * 50 + 200}ms` }}
                >
                  {food.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Food Detail Panel */}
        <div className="flex-1">
          <div 
            className={`
              h-full min-h-[450px] rounded-xl border-2 overflow-hidden
              transition-all duration-300 ease-out
              ${selectedFood && selectedRing
                ? `${ringColors[selectedRing].border} ${ringColors[selectedRing].bgLight}`
                : 'border-border bg-muted/30'
              }
            `}
          >
            {selectedFood ? (
              <div className="animate-fade-in h-full flex flex-col">
                {/* Food Image */}
                <div className="relative h-56 overflow-hidden">
                  <img
                    src={selectedFood.imageUrl}
                    alt={selectedFood.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4">
                    <div className="flex items-center gap-2 mb-1">
                      {selectedRing && (
                        <span className={`px-2 py-0.5 rounded-full text-xs font-semibold text-white ${ringColors[selectedRing].bg}`}>
                          {selectedRing === 'core' ? 'Core Comfort' : selectedRing === 'stretch' ? 'Safe Stretch' : 'Experimental'}
                        </span>
                      )}
                    </div>
                    <h3 className="font-display text-2xl font-bold text-white">
                      {selectedFood.name}
                    </h3>
                  </div>
                </div>

                {/* Food Details */}
                <div className="p-5 flex-1 flex flex-col">
                  {/* Origin Info */}
                  <div className="flex flex-wrap gap-4 mb-4">
                    <div className="flex items-center gap-2">
                      <Globe className="w-4 h-4 text-muted-foreground" />
                      <span className="text-sm font-medium text-foreground">{selectedFood.origin}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-muted-foreground" />
                      <span className="text-sm text-muted-foreground">{selectedFood.region}</span>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-foreground leading-relaxed flex-1">
                    {selectedFood.description}
                  </p>
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center p-6">
                <div className="w-16 h-16 rounded-full bg-muted/50 flex items-center justify-center mb-4">
                  <span className="text-3xl">🍽️</span>
                </div>
                <p className="text-muted-foreground font-medium mb-1">Select a food to explore</p>
                <p className="text-sm text-muted-foreground/70">
                  Click on any food from the list to see its image, origin, and history
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
