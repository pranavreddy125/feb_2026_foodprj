import { ARCHETYPES, ArchetypeId } from '@/lib/food-data';

interface ArchetypeSelectProps {
  selected: ArchetypeId[];
  onChange: (archetypes: ArchetypeId[]) => void;
}

export function ArchetypeSelect({ selected, onChange }: ArchetypeSelectProps) {
  const toggleArchetype = (id: ArchetypeId) => {
    if (selected.includes(id)) {
      onChange(selected.filter(a => a !== id));
    } else {
      onChange([...selected, id]);
    }
  };

  return (
    <div className="space-y-3">
      <div>
        <h3 className="font-semibold text-foreground">Self-Identified Archetypes</h3>
        <p className="text-sm text-muted-foreground">Select any that resonate with you (optional)</p>
      </div>
      
      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {ARCHETYPES.map((archetype) => (
          <button
            key={archetype.id}
            type="button"
            onClick={() => toggleArchetype(archetype.id)}
            data-selected={selected.includes(archetype.id)}
            className="multi-select-chip text-left p-3 rounded-lg"
          >
            <div className="font-medium">{archetype.label}</div>
            <div className="text-xs text-muted-foreground mt-0.5">{archetype.description}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
