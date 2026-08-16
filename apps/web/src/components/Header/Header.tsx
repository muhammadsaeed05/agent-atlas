import React from 'react';
import { Compass, User } from 'lucide-react';

interface HeaderProps {
  onPlanTripClick?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onPlanTripClick }) => {
  return (
    <header className="bg-surface/90 backdrop-blur-md sticky top-0 z-50 border-b border-sand/40 transition-all duration-300">
      <div className="flex justify-between items-center w-full px-5 md:px-20 py-5 max-w-screen-2xl mx-auto">
        {/* Brand Logo & Title */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <div className="w-10 h-10 rounded-full bg-sand/30 border border-sand flex items-center justify-center text-earthy-green shadow-xs">
            <Compass className="w-6 h-6 text-earthy-green animate-[spin_30s_linear_infinite]" />
          </div>
          <span className="font-headline text-2xl md:text-[28px] font-semibold text-primary tracking-tight">
            Agent Atlas
          </span>
        </div>

        {/* Center Nav Links (Editorial Caps) */}
        <nav className="hidden md:flex gap-8 items-center">
          <a
            href="#destinations"
            onClick={(e) => e.preventDefault()}
            className="text-[12px] uppercase font-semibold tracking-[0.1em] text-outline hover:text-primary transition-colors duration-200 cursor-pointer"
          >
            Destinations
          </a>
          <a
            href="#curator"
            className="text-[12px] uppercase font-semibold tracking-[0.1em] text-primary border-b-2 border-primary pb-1 cursor-pointer"
          >
            Curator
          </a>
          <a
            href="#journal"
            onClick={(e) => e.preventDefault()}
            className="text-[12px] uppercase font-semibold tracking-[0.1em] text-outline hover:text-primary transition-colors duration-200 cursor-pointer"
          >
            Journal
          </a>
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-4">
          <button
            onClick={onPlanTripClick}
            className="hidden sm:flex items-center justify-center text-[14px] font-medium bg-earthy-green text-on-primary px-6 py-2.5 rounded-DEFAULT hover:opacity-90 active:scale-[0.98] transition-all shadow-sm"
          >
            Plan Trip
          </button>
          <button
            type="button"
            aria-label="User Account"
            className="w-10 h-10 rounded-full flex items-center justify-center text-primary/80 hover:text-primary hover:bg-sand/20 transition-colors"
          >
            <User className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
};
