import { useState, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { DimensionSelector } from "@/components/DimensionSelector";
import { FoodMultiSelect } from "@/components/FoodMultiSelect";
import { ArchetypeSelect } from "@/components/ArchetypeSelect";
import { ResultsDisplay } from "@/components/ResultsDisplay";
import { CatMascot } from "@/components/CatMascot";
import { computeFoodPersonality } from "@/lib/food-api";
import {
  TasteDimensions,
  Food,
  ArchetypeId,
  PersonalityResult,
  TASTE_DIMENSIONS,
  FOODS,
  ARCHETYPES,
} from "@/lib/food-data";
import { Loader2, UtensilsCrossed } from "lucide-react";

type PartialDimensions = {
  [K in keyof TasteDimensions]: number | null;
};

export default function Index() {
  const [dimensions, setDimensions] = useState<PartialDimensions>({
    spice_intensity: null,
    texture_intensity: null,
    preparation_familiarity: null,
    richness: null,
    psychological_distance: null,
  });
  const [dislikes, setDislikes] = useState<Food[]>([]);
  const [archetypes, setArchetypes] = useState<ArchetypeId[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PersonalityResult | null>(null);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};
    setSubmitError(null);

    TASTE_DIMENSIONS.forEach((dim) => {
      const value = dimensions[dim.id as keyof TasteDimensions];
      if (value === null) {
        newErrors[dim.id] = `${dim.label} is required`;
      } else if (![0.2, 0.5, 0.8].includes(value)) {
        newErrors[dim.id] = "Invalid value selected";
      }
    });

    const validFoods = new Set(FOODS);
    const validArchetypes = new Set(ARCHETYPES.map((item) => item.id));
    let selectionError = "";

    if (dislikes.some((food) => !validFoods.has(food))) {
      selectionError = "Please remove any invalid food dislikes before submitting.";
    }

    if (archetypes.some((archetype) => !validArchetypes.has(archetype))) {
      selectionError = "Please remove any invalid archetypes before submitting.";
    }

    if (selectionError) {
      setSubmitError(selectionError);
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0 && !selectionError;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setResult(null);
    setSubmitError(null);

    try {
      const response = await computeFoodPersonality({
        tasteDimensions: dimensions as TasteDimensions,
        dislikes,
        archetypes,
      });
      setResult(response);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to reach the backend. Please try again.";
      setSubmitError(message);
      console.error("Error computing personality:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateDimension = (id: keyof TasteDimensions, value: number) => {
    setDimensions((prev) => ({ ...prev, [id]: value }));
    if (errors[id]) {
      setErrors((prev) => {
        const updated = { ...prev };
        delete updated[id];
        return updated;
      });
    }
  };

  const handleReset = () => {
    setResult(null);
    setDimensions({
      spice_intensity: null,
      texture_intensity: null,
      preparation_familiarity: null,
      richness: null,
      psychological_distance: null,
    });
    setDislikes([]);
    setArchetypes([]);
    setErrors({});
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Count selections for cat mascot
  const selectionCount = useMemo(() => {
    const dimensionCount = Object.values(dimensions).filter((v) => v !== null).length;
    const archetypeCount = Math.min(archetypes.length, 2); // Cap at 2 for variety
    return dimensionCount + archetypeCount;
  }, [dimensions, archetypes]);

  return (
    <div className="min-h-screen bg-background">
      {/* Cat Mascot - only on form page */}
      {!result && <CatMascot filledCount={selectionCount} maxCount={7} />}

      {/* Results View - Full width */}
      {result ? (
        <div className="min-h-screen">
          {/* Results Hero */}
          <div className="relative overflow-hidden bg-gradient-to-br from-primary/10 via-ring-core/5 to-ring-stretch/10 pt-12 pb-20 sm:pt-16 sm:pb-24">
            {/* Decorative Elements */}
            <div className="absolute top-10 left-10 w-40 h-40 rounded-full bg-ring-core/15 blur-3xl animate-pulse" />
            <div
              className="absolute top-20 right-20 w-48 h-48 rounded-full bg-ring-stretch/15 blur-3xl animate-pulse"
              style={{ animationDelay: "1s" }}
            />
            <div
              className="absolute bottom-10 left-1/4 w-32 h-32 rounded-full bg-ring-experimental/15 blur-2xl animate-pulse"
              style={{ animationDelay: "2s" }}
            />

            {/* Celebration Emojis */}
            <div
              className="absolute top-16 left-[10%] text-4xl opacity-30 animate-bounce"
              style={{ animationDelay: "0s" }}
            >
              🎉
            </div>
            <div
              className="absolute top-28 right-[15%] text-3xl opacity-30 animate-bounce"
              style={{ animationDelay: "0.5s" }}
            >
              🍽️
            </div>
            <div
              className="absolute bottom-24 left-[20%] text-3xl opacity-30 animate-bounce"
              style={{ animationDelay: "1s" }}
            >
              ✨
            </div>
            <div
              className="absolute bottom-16 right-[25%] text-4xl opacity-30 animate-bounce"
              style={{ animationDelay: "1.5s" }}
            >
              🎊
            </div>

            <div className="container max-w-4xl px-4 sm:px-6 relative z-10">
              <div className="text-center">

                <h1
                  className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-foreground mb-4 animate-fade-in"
                  style={{ animationDelay: "100ms" }}
                >
                  We've Cracked
                  <span className="block bg-gradient-to-r from-ring-core via-ring-stretch to-ring-experimental bg-clip-text text-transparent">
                    Your Food Code!
                  </span>
                </h1>

                <p
                  className="text-muted-foreground text-lg sm:text-xl max-w-2xl mx-auto animate-fade-in"
                  style={{ animationDelay: "200ms" }}
                >
                  Based on your preferences, here's your unique food personality profile.
                </p>
              </div>
            </div>
          </div>

          {/* Results Content */}
          <div className="container max-w-7xl px-4 sm:px-6 lg:px-8 py-12 -mt-10">
            <div className="space-y-8">
              <ResultsDisplay result={result} />
              <div className="text-center pt-6 animate-fade-in" style={{ animationDelay: "500ms" }}>
                <Button
                  onClick={handleReset}
                  variant="outline"
                  size="lg"
                  className="min-w-[200px] hover:scale-[1.02] transition-transform"
                >
                  Start Over
                </Button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Form View - Personality-filled */
        <>
          {/* Hero Section */}
          <div className="relative overflow-hidden bg-gradient-to-br from-primary/5 via-background to-ring-core/5 pt-12 pb-16 sm:pt-16 sm:pb-20">
            {/* Decorative Elements */}
            <div className="absolute top-10 left-10 w-32 h-32 rounded-full bg-ring-core/10 blur-3xl animate-pulse" />
            <div
              className="absolute top-20 right-20 w-40 h-40 rounded-full bg-ring-stretch/10 blur-3xl animate-pulse"
              style={{ animationDelay: "1s" }}
            />
            <div
              className="absolute bottom-10 left-1/3 w-24 h-24 rounded-full bg-ring-experimental/10 blur-2xl animate-pulse"
              style={{ animationDelay: "2s" }}
            />

            {/* Floating Food Emojis */}
            <div
              className="absolute top-16 left-[15%] text-4xl opacity-20 animate-bounce"
              style={{ animationDelay: "0.5s" }}
            >
              🌶️
            </div>
            <div
              className="absolute top-24 right-[20%] text-3xl opacity-20 animate-bounce"
              style={{ animationDelay: "1s" }}
            >
              🍜
            </div>
            <div
              className="absolute bottom-20 left-[25%] text-3xl opacity-20 animate-bounce"
              style={{ animationDelay: "1.5s" }}
            >
              🥑
            </div>
            <div
              className="absolute bottom-16 right-[30%] text-4xl opacity-20 animate-bounce"
              style={{ animationDelay: "2s" }}
            >
              🍕
            </div>

            <div className="container max-w-4xl px-4 sm:px-6 relative z-10">
              <div className="text-center">
                {/* Animated Icon */}
                <div className="inline-flex items-center justify-center w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-gradient-to-br from-primary to-primary/80 shadow-xl shadow-primary/30 mb-6 animate-fade-in">
                  <UtensilsCrossed className="w-10 h-10 sm:w-12 sm:h-12 text-primary-foreground" />
                </div>

                <h1
                  className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-foreground mb-4 animate-fade-in"
                  style={{ animationDelay: "100ms" }}
                >
                  What's Your
                  <span className="block bg-gradient-to-r from-primary via-ring-stretch to-ring-experimental bg-clip-text text-transparent">
                    Food Personality?
                  </span>
                </h1>

                <p
                  className="text-muted-foreground text-lg sm:text-xl max-w-2xl mx-auto mb-8 animate-fade-in"
                  style={{ animationDelay: "200ms" }}
                >
                  Everyone has a unique relationship with food. Discover yours—from comfort cravings to culinary
                  adventures.
                </p>

                {/* Feature Pills */}
                <div
                  className="flex flex-wrap justify-center gap-3 animate-fade-in"
                  style={{ animationDelay: "300ms" }}
                >
                  {[
                    { emoji: "🎯", text: "Personalized Results" },
                    { emoji: "🔥", text: "Spice Tolerance" },
                    { emoji: "🌍", text: "Cuisine Matching" },
                  ].map((item, i) => (
                    <div
                      key={item.text}
                      className="flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border shadow-sm"
                    >
                      <span>{item.emoji}</span>
                      <span className="text-sm font-medium text-foreground">{item.text}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Form Section */}
          <div className="container max-w-6xl px-4 sm:px-6 lg:px-8 py-12 -mt-6">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Taste Dimensions */}
              <section className="section-card space-y-6 animate-fade-in" style={{ animationDelay: "400ms" }}>
                <div className="flex items-start gap-4">
                  <div className="hidden sm:flex w-12 h-12 rounded-xl bg-primary/10 items-center justify-center flex-shrink-0">
                    <span className="text-2xl">🎚️</span>
                  </div>
                  <div>
                    <h2 className="font-display text-xl sm:text-2xl font-bold text-foreground">
                      Your Taste Dimensions
                    </h2>
                    <p className="text-sm text-muted-foreground mt-1">
                      How adventurous is your palate? Set your preferences below.
                    </p>
                  </div>
                </div>

                <div className="space-y-5">
                  {TASTE_DIMENSIONS.map((dim, index) => (
                    <div key={dim.id} className="animate-fade-in" style={{ animationDelay: `${500 + index * 80}ms` }}>
                      <DimensionSelector
                        dimensionId={dim.id}
                        value={dimensions[dim.id as keyof TasteDimensions]}
                        onChange={(value) => updateDimension(dim.id as keyof TasteDimensions, value)}
                        error={errors[dim.id]}
                      />
                    </div>
                  ))}
                </div>
              </section>

              {/* Dislikes */}
              <section className="section-card animate-fade-in" style={{ animationDelay: "900ms" }}>
                <div className="flex items-start gap-4 mb-4">
                  <div className="hidden sm:flex w-12 h-12 rounded-xl bg-destructive/10 items-center justify-center flex-shrink-0">
                    <span className="text-2xl">🙅</span>
                  </div>
                  <div className="flex-1">
                    <FoodMultiSelect
                      selected={dislikes}
                      onChange={setDislikes}
                      label="No Thanks, Not For Me"
                      description="Any foods you'd rather skip? (totally optional)"
                    />
                  </div>
                </div>
              </section>

              {/* Archetypes */}
              <section className="section-card animate-fade-in" style={{ animationDelay: "1000ms" }}>
                <div className="flex items-start gap-4 mb-4">
                  <div className="hidden sm:flex w-12 h-12 rounded-xl bg-ring-stretch/20 items-center justify-center flex-shrink-0">
                    <span className="text-2xl">✨</span>
                  </div>
                  <div className="flex-1">
                    <ArchetypeSelect selected={archetypes} onChange={setArchetypes} />
                  </div>
                </div>
              </section>

              {/* Submit */}
              <div className="text-center pt-4 animate-fade-in" style={{ animationDelay: "1100ms" }}>
                <Button
                  type="submit"
                  size="lg"
                  disabled={isLoading}
                  className="min-w-[280px] h-14 text-lg shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30 transition-all duration-300 hover:scale-[1.02]"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Analyzing Your Taste...
                    </>
                  ) : (
                    <>🍽️ Discover My Food Personality</>
                  )}
                </Button>

                {Object.keys(errors).length > 0 && (
                  <p className="text-sm text-destructive mt-3 animate-fade-in">
                    Hold up! Please complete all the taste dimensions above ☝️
                  </p>
                )}
                {submitError && (
                  <p className="text-sm text-destructive mt-3 animate-fade-in">
                    {submitError}
                  </p>
                )}

                <p className="text-xs text-muted-foreground mt-4"></p>
              </div>
            </form>
          </div>
        </>
      )}
    </div>
  );
}
