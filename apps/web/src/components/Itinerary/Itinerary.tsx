import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Printer, RotateCcw, Sparkles } from 'lucide-react';

interface ItineraryProps {
  content: string;
  onReset?: () => void;
}

export const Itinerary: React.FC<ItineraryProps> = ({ content, onReset }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch {
      // Fallback
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <section
      id="itinerary-results"
      className="max-w-5xl mx-auto w-full animate-fade-in transition-all duration-700"
    >
      {/* Top Utility / Action Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b border-sand/40">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-earthy-green/10 text-earthy-green text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" />
            Curated Itinerary
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-DEFAULT border border-sand/60 text-xs font-medium text-primary hover:bg-sand/20 active:scale-95 transition-all"
            title="Copy markdown text"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-earthy-green" />
                <span className="text-earthy-green">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-secondary" />
                <span>Copy</span>
              </>
            )}
          </button>

          <button
            type="button"
            onClick={handlePrint}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-DEFAULT border border-sand/60 text-xs font-medium text-primary hover:bg-sand/20 active:scale-95 transition-all"
            title="Print or Save as PDF"
          >
            <Printer className="w-3.5 h-3.5 text-secondary" />
            <span>Print</span>
          </button>

          {onReset && (
            <button
              type="button"
              onClick={onReset}
              className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-DEFAULT border border-sand/60 text-xs font-medium text-primary hover:bg-sand/20 active:scale-95 transition-all"
              title="New Itinerary"
            >
              <RotateCcw className="w-3.5 h-3.5 text-secondary" />
              <span>New Search</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Journal Parchment Canvas */}
      <div className="bg-surface-container-lowest border border-sand rounded-xl p-6 sm:p-10 md:p-14 shadow-subtle relative overflow-hidden">
        {/* Subtle Map Topographic Background Contour Texture */}
        <div className="contour-overlay" />

        {/* Content Container */}
        <div className="relative z-10 journal-prose max-w-none">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ children }) => (
                <h1 className="font-display text-3xl sm:text-4xl md:text-[42px] md:leading-[50px] font-bold text-primary mb-3 mt-2 tracking-tight">
                  {children}
                </h1>
              ),
              h2: ({ children }) => {
                const text = String(children);
                const isDay = text.toLowerCase().includes('day') || text.includes('📍');
                return (
                  <div className="relative my-8 pt-4">
                    {isDay && (
                      <div className="flex items-center gap-3">
                        <span className="w-3 h-3 rounded-full bg-earthy-green inline-block flex-shrink-0 shadow-xs" />
                        <h2 className="font-display text-2xl sm:text-[28px] font-semibold text-primary my-0 border-none pb-0 tracking-tight">
                          {children}
                        </h2>
                      </div>
                    )}
                    {!isDay && (
                      <h2 className="font-display text-2xl sm:text-[28px] font-semibold text-primary mt-6 mb-4 pb-2 border-b border-sand/40 tracking-tight">
                        {children}
                      </h2>
                    )}
                  </div>
                );
              },
              h3: ({ children }) => (
                <h3 className="font-display text-xl sm:text-2xl font-medium text-primary mt-6 mb-3 tracking-tight">
                  {children}
                </h3>
              ),
              h4: ({ children }) => (
                <h4 className="font-sans text-xs uppercase font-semibold tracking-[0.12em] text-outline mt-5 mb-2">
                  {children}
                </h4>
              ),
              p: ({ children }) => (
                <p className="font-sans text-base sm:text-[17px] text-[#333232] leading-relaxed mb-4">
                  {children}
                </p>
              ),
              blockquote: ({ children }) => (
                <blockquote className="my-6 border-l-4 border-terracotta bg-sand/15 rounded-r-lg p-5 sm:p-6 text-base sm:text-lg italic text-[#2D4739] shadow-xs">
                  {children}
                </blockquote>
              ),
              ul: ({ children }) => (
                <ul className="space-y-2.5 my-4 pl-0 list-none font-sans text-base text-[#333232]">
                  {children}
                </ul>
              ),
              li: ({ children }) => (
                <li className="relative pl-6 leading-relaxed">
                  <span className="absolute left-0 top-1 text-terracotta font-bold text-sm">
                    ✦
                  </span>
                  <div>{children}</div>
                </li>
              ),
              ol: ({ children }) => (
                <ol className="space-y-2.5 my-4 pl-5 list-decimal font-sans text-base text-[#333232]">
                  {children}
                </ol>
              ),
              strong: ({ children }) => (
                <strong className="font-semibold text-primary">
                  {children}
                </strong>
              ),
              em: ({ children }) => (
                <em className="italic text-terracotta font-medium">
                  {children}
                </em>
              ),
              hr: () => (
                <hr className="my-8 border-0 border-t border-sand/40" />
              ),
              table: ({ children }) => (
                <div className="overflow-x-auto my-6 rounded-lg border border-sand">
                  <table className="w-full text-left text-sm font-sans">{children}</table>
                </div>
              ),
              th: ({ children }) => (
                <th className="bg-sand/30 font-semibold text-primary uppercase text-xs tracking-wider p-3.5 border-b border-sand">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="p-3.5 border-b border-sand/40 text-primary">
                  {children}
                </td>
              ),
              a: ({ href, children }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-terracotta underline decoration-terracotta/40 underline-offset-4 hover:decoration-terracotta transition-all"
                >
                  {children}
                </a>
              ),
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>
    </section>
  );
};
