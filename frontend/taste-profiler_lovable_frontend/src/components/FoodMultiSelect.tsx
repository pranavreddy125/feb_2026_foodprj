import { FOODS, Food } from '@/lib/food-data';

interface FoodMultiSelectProps {
  selected: Food[];
  onChange: (foods: Food[]) => void;
  label: string;
  description: string;
}

export function FoodMultiSelect({ selected, onChange, label, description }: FoodMultiSelectProps) {
  const toggleFood = (food: Food) => {
    if (selected.includes(food)) {
      onChange(selected.filter(f => f !== food));
    } else {
      onChange([...selected, food]);
    }
  };

  return (
    <div className="space-y-3">
      <div>
        <h3 className="font-semibold text-foreground">{label}</h3>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
      
      <div className="flex flex-wrap gap-2">
        {FOODS.map((food) => (
          <button
            key={food}
            type="button"
            onClick={() => toggleFood(food)}
            data-selected={selected.includes(food)}
            className="multi-select-chip"
          >
            {food}
            {selected.includes(food) && (
              <span className="text-primary">✓</span>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}
