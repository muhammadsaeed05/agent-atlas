import { Compass, Sparkles } from 'lucide-react';
import { MOCK_SUGGESTIONS } from '../../services/mockData';

interface TravelPromptProps {
  prompt: string;
  setPrompt: (value: string) => void;
  onGenerate: () => void;
  isGenerating: boolean;
}

export const TravelPrompt: React.FC<TravelPromptProps> = ({
  prompt,
  setPrompt,
  onGenerate,
  isGenerating,
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      if (!isGenerating && prompt.trim()) {
        onGenerate();
      }
    }
  };

  return (
    <section className="max-w-4xl mx-auto w-full text-center mb-12 md:mb-16">
      {/* Hero Title & Subtitle */}
      <h1 className="font-display text-4xl sm:text-5xl md:text-[64px] md:leading-[72px] font-bold text-primary mb-5 tracking-[-0.02em]">
        Plan your next adventure.
      </h1>
      <p className="font-sans text-lg md:text-xl text-secondary max-w-2xl mx-auto mb-10 leading-relaxed">
        Tell Agent Atlas where you want to go, what you love, and how you want to travel.
      </p>

      {/* Main Prompt Card */}
      <div className="relative w-full mb-6 text-left group">
        <div className="relative bg-surface-container-lowest border border-sand rounded-xl shadow-subtle hover:border-sand/80 focus-within:border-earthy-green focus-within:ring-1 focus-within:ring-earthy-green transition-all duration-300 overflow-hidden">
          <textarea
            id="prompt-input"
            rows={5}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isGenerating}
            placeholder="Plan a 7-day trip to Japan for two people, focusing on food, culture, photography, and hidden gems..."
            className="w-full bg-transparent p-6 md:p-8 font-sans text-base md:text-lg text-primary placeholder:text-outline/70 resize-none focus:outline-none disabled:opacity-60 min-h-[190px]"
          />

          {/* Action Bar inside textarea container */}
          <div className="flex flex-col sm:flex-row justify-between items-center px-6 pb-6 pt-2 border-t border-sand/20 gap-3">
            <span className="text-xs font-sans text-outline/80 hidden sm:inline-flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-terracotta" />
              Pro-tip: Include duration, traveler count, and interests for richer itineraries
            </span>

            <button
              id="generate-btn"
              type="button"
              onClick={onGenerate}
              disabled={isGenerating || !prompt.trim()}
              className="w-full sm:w-auto font-sans text-sm font-medium bg-earthy-green text-on-primary px-8 py-3.5 rounded-DEFAULT hover:opacity-90 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center gap-2.5 shadow-md ml-auto"
            >
              {isGenerating ? (
                <>
                  <Compass className="w-4 h-4 animate-spin text-on-primary" />
                  <span>Planning Journey...</span>
                </>
              ) : (
                <>
                  <span>Generate Itinerary</span>
                  <Compass className="w-4 h-4 text-on-primary" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Suggestion Chips */}
      <div className="flex flex-wrap justify-center gap-2.5 sm:gap-3">
        {MOCK_SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion.id}
            type="button"
            onClick={() => setPrompt(suggestion.prompt)}
            disabled={isGenerating}
            className="suggestion-chip font-sans text-[12px] uppercase font-semibold tracking-[0.08em] bg-sand/25 text-primary px-4 py-2 rounded-full border border-sand hover:bg-sand/45 active:scale-95 disabled:opacity-50 transition-all duration-200 text-left"
          >
            {suggestion.label}
          </button>
        ))}
      </div>
    </section>
  );
};
