import React, { useState, useRef } from 'react';
import { Header } from './components/Header/Header';
import { TravelPrompt } from './components/TravelPrompt/TravelPrompt';
import { LoadingState } from './components/LoadingState/LoadingState';
import { Itinerary } from './components/Itinerary/Itinerary';
import { Footer } from './components/Footer/Footer';
import { generateItinerary } from './services/itinerary';
import { GenerationStatus } from './types/itinerary';
import { AlertCircle } from 'lucide-react';

export const App: React.FC = () => {
  const [prompt, setPrompt] = useState<string>('');
  const [status, setStatus] = useState<GenerationStatus>('idle');
  const [itineraryContent, setItineraryContent] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const promptSectionRef = useRef<HTMLDivElement>(null);
  const itinerarySectionRef = useRef<HTMLDivElement>(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setStatus('loading');
    setErrorMessage(null);

    try {
      const response = await generateItinerary({
        message: prompt.trim(),
      });

      setItineraryContent(response.reply);
      setStatus('success');

      // Smooth scroll to generated itinerary
      setTimeout(() => {
        itinerarySectionRef.current?.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      }, 100);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'An unexpected error occurred while generating your itinerary.';
      setErrorMessage(message);
      setStatus('error');
    }
  };

  const handleReset = () => {
    setPrompt('');
    setItineraryContent('');
    setStatus('idle');
    setErrorMessage(null);
    promptSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handlePlanTripClick = () => {
    promptSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
    const textarea = document.getElementById('prompt-input') as HTMLTextAreaElement | null;
    textarea?.focus();
  };

  return (
    <div className="min-h-screen flex flex-col bg-background text-primary selection:bg-sand/40 selection:text-primary">
      {/* Top Header */}
      <Header onPlanTripClick={handlePlanTripClick} />

      {/* Main Content Area */}
      <main className="flex-grow flex flex-col w-full max-w-screen-2xl mx-auto px-5 md:px-20 py-10 md:py-16">
        <div ref={promptSectionRef} id="curator">
          <TravelPrompt
            prompt={prompt}
            setPrompt={setPrompt}
            onGenerate={handleGenerate}
            isGenerating={status === 'loading'}
          />
        </div>

        {/* Error Alert */}
        {status === 'error' && errorMessage && (
          <div className="max-w-4xl mx-auto w-full mb-8 p-4 bg-error-container/30 border border-error/20 rounded-lg flex items-center gap-3 text-error animate-fade-in">
            <AlertCircle className="w-5 h-5 flex-shrink-0 text-error" />
            <p className="font-sans text-sm">{errorMessage}</p>
          </div>
        )}

        {/* Loading State */}
        {status === 'loading' && <LoadingState />}

        {/* Itinerary Results */}
        {status === 'success' && itineraryContent && (
          <div ref={itinerarySectionRef} className="pt-4">
            <Itinerary content={itineraryContent} onReset={handleReset} />
          </div>
        )}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default App;
