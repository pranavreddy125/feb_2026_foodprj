import { useState, useEffect } from 'react';
import { PersonalityResult } from '@/lib/food-data';
import { ComfortRingsVisualization } from './ComfortRingsVisualization';
import { Sparkles, TrendingUp, Star } from 'lucide-react';

interface ResultsDisplayProps {
  result: PersonalityResult;
}

const PERSONALITY_EMOJIS: Record<string, string> = {
  'Comfort Seeker': '🏠',
  'Spice Lover': '🌶️',
  'Texture Explorer': '🥢',
  'Adventurous Eater': '🌍',
  'Minimalist': '🧘',
  'Balanced Eater': '⚖️',
  'Rich Food Lover': '🍰',
  'Familiar First': '🥔',
  'Global Palate': '✈️',
  default: '🍽️',
};

function ConfidenceMeter({ value, color }: { value: number; color: string }) {
  const [animatedValue, setAnimatedValue] = useState(0);
  
  useEffect(() => {
    const timer = setTimeout(() => setAnimatedValue(value * 100), 100);
    return () => clearTimeout(timer);
  }, [value]);

  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-muted-foreground">Confidence</span>
        <span className="font-semibold">{animatedValue.toFixed(0)}%</span>
      </div>
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <div 
          className={`h-full rounded-full transition-all duration-1000 ease-out ${color}`}
          style={{ width: `${animatedValue}%` }}
        />
      </div>
    </div>
  );
}

export function ResultsDisplay({ result }: ResultsDisplayProps) {
  const primaryEmoji = PERSONALITY_EMOJIS[result.primaryPersonality] || PERSONALITY_EMOJIS['default'];
  const secondaryEmoji = result.secondaryPersonality 
    ? PERSONALITY_EMOJIS[result.secondaryPersonality] || PERSONALITY_EMOJIS['default']
    : null;

  return (
    <div className="space-y-8">
      {/* Personality Section - Redesigned */}
      <div className="animate-fade-in">
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Primary Personality Card */}
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-primary/5 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-500" />
            <div className="relative section-card border-2 border-primary/30 hover:border-primary/50 transition-all duration-300 h-full">
              {/* Badge */}
              <div className="absolute -top-3 left-6">
                <div className="flex items-center gap-1.5 px-3 py-1 bg-primary text-primary-foreground rounded-full text-xs font-bold shadow-lg">
                  <Star className="w-3 h-3" />
                  PRIMARY TYPE
                </div>
              </div>
              
              <div className="pt-4">
                <div className="flex items-start gap-4">
                  {/* Icon */}
                  <div className="flex-shrink-0 w-20 h-20 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center hover:scale-110 transition-transform duration-300">
                    <Sparkles className="w-10 h-10 text-primary" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="font-display text-2xl sm:text-3xl font-bold text-foreground mb-1 truncate">
                      {result.primaryPersonality}
                    </h3>
                    <ConfidenceMeter value={result.primaryConfidence} color="bg-primary" />
                  </div>
                </div>
                
                {/* Traits */}
                <div className="mt-4 flex flex-wrap gap-2">
                  {['Bold Choices', 'Flavor Forward', 'Adventurous'].map((trait, i) => (
                    <span 
                      key={trait}
                      className="px-3 py-1 bg-primary/10 text-primary rounded-full text-xs font-medium animate-fade-in"
                      style={{ animationDelay: `${300 + i * 100}ms` }}
                    >
                      {trait}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
          
          {/* Secondary Personality Card */}
          {result.secondaryPersonality && (
            <div className="relative group animate-fade-in" style={{ animationDelay: '150ms' }}>
              <div className="absolute inset-0 bg-gradient-to-br from-ring-stretch/20 to-ring-stretch/5 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-500" />
              <div className="relative section-card border-2 border-ring-stretch/30 hover:border-ring-stretch/50 transition-all duration-300 h-full">
                {/* Badge */}
                <div className="absolute -top-3 left-6">
                  <div className="flex items-center gap-1.5 px-3 py-1 bg-ring-stretch text-white rounded-full text-xs font-bold shadow-lg">
                    <TrendingUp className="w-3 h-3" />
                    SECONDARY TYPE
                  </div>
                </div>
                
                <div className="pt-4">
                  <div className="flex items-start gap-4">
                    {/* Icon */}
                    <div className="flex-shrink-0 w-20 h-20 rounded-2xl bg-gradient-to-br from-ring-stretch/20 to-ring-stretch/5 flex items-center justify-center hover:scale-110 transition-transform duration-300">
                      <TrendingUp className="w-10 h-10 text-ring-stretch" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <h3 className="font-display text-2xl sm:text-3xl font-bold text-foreground mb-1 truncate">
                        {result.secondaryPersonality}
                      </h3>
                      <ConfidenceMeter value={result.secondaryConfidence || 0} color="bg-ring-stretch" />
                    </div>
                  </div>
                  
                  {/* Traits */}
                  <div className="mt-4 flex flex-wrap gap-2">
                    {['Balanced', 'Open-minded', 'Curious'].map((trait, i) => (
                      <span 
                        key={trait}
                        className="px-3 py-1 bg-ring-stretch/10 text-ring-stretch rounded-full text-xs font-medium animate-fade-in"
                        style={{ animationDelay: `${450 + i * 100}ms` }}
                      >
                        {trait}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Explanation Card */}
        <div 
          className="mt-6 section-card bg-gradient-to-r from-muted/50 to-muted/30 border-dashed animate-fade-in"
          style={{ animationDelay: '300ms' }}
        >
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h4 className="font-display font-semibold text-foreground mb-1">What This Means</h4>
              <p className="text-muted-foreground leading-relaxed">
                {result.explanation}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Comfort Rings Visualization - UNCHANGED */}
      <div 
        className="animate-fade-in"
        style={{ animationDelay: '400ms' }}
      >
        <ComfortRingsVisualization result={result} />
      </div>
    </div>
  );
}
