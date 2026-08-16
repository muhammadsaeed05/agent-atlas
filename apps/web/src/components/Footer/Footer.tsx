import React from 'react';
import { Compass } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-surface-container-lowest border-t border-sand/40 w-full mt-16 md:mt-24">
      <div className="flex flex-col md:flex-row justify-between items-center w-full px-5 md:px-20 py-12 max-w-screen-2xl mx-auto">
        <div className="flex flex-col items-center md:items-start gap-2 mb-8 md:mb-0">
          <div className="flex items-center gap-2.5">
            <Compass className="w-5 h-5 text-earthy-green" />
            <span className="font-headline text-2xl font-semibold text-primary">
              Agent Atlas
            </span>
          </div>
          <span className="text-[12px] uppercase font-semibold tracking-[0.1em] text-secondary">
            © {new Date().getFullYear()} Agent Atlas. A Curated Travel Experience.
          </span>
        </div>

        <nav className="flex flex-wrap justify-center gap-6 md:gap-8">
          <a
            href="#privacy"
            onClick={(e) => e.preventDefault()}
            className="text-[12px] uppercase font-semibold tracking-[0.1em] text-secondary hover:text-primary transition-colors duration-200"
          >
            Privacy Policy
          </a>
          <a
            href="#terms"
            onClick={(e) => e.preventDefault()}
            className="text-[12px] uppercase font-semibold tracking-[0.1em] text-secondary hover:text-primary transition-colors duration-200"
          >
            Terms of Service
          </a>
          <a
            href="#archives"
            onClick={(e) => e.preventDefault()}
            className="text-[12px] uppercase font-semibold tracking-[0.1em] text-secondary hover:text-primary transition-colors duration-200"
          >
            Journal Archives
          </a>
          <a
            href="#contact"
            onClick={(e) => e.preventDefault()}
            className="text-[12px] uppercase font-semibold tracking-[0.1em] text-secondary hover:text-primary transition-colors duration-200"
          >
            Contact
          </a>
        </nav>
      </div>
    </footer>
  );
};
