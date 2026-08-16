import React from 'react';

export const LoadingState: React.FC = () => {
  return (
    <div
      id="loading-state"
      className="flex flex-col items-center justify-center py-12 md:py-16 animate-fade-in text-center max-w-lg mx-auto"
    >
      {/* Animated SVG Travel Route from Stitch design */}
      <div className="relative w-32 h-32 mb-6">
        <svg
          viewBox="0 0 200 200"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full drop-shadow-xs"
        >
          {/* Subtle Outer Boundary Indicator */}
          <circle cx="100" cy="100" r="85" fill="none" stroke="#D9C5B2" strokeWidth="0.8" opacity="0.35" strokeDasharray="3 3" />
          
          {/* Curved Dotted Flight/Train Route */}
          <path
            d="M40 100 Q 70 50, 100 100 T 160 100"
            fill="none"
            stroke="#D9C5B2"
            strokeDasharray="4 4"
            strokeWidth="2.5"
          />

          {/* Animated Waypoint Location Marker / Pin */}
          <g>
            <circle cx="0" cy="0" fill="#CC4F36" r="4.5">
              <animateMotion
                dur="3s"
                path="M40 100 Q 70 50, 100 100 T 160 100"
                repeatCount="indefinite"
              />
            </circle>
            {/* Minimalist Pin glyph */}
            <path d="M0 -2 L2 -7 A2.5 2.5 0 0 0 -2 -7 L0 -2" fill="#CC4F36">
              <animateMotion
                dur="3s"
                path="M40 100 Q 70 50, 100 100 T 160 100"
                repeatCount="indefinite"
              />
            </path>
          </g>

          {/* Pulse at Origin (Day 1) */}
          <circle cx="40" cy="100" fill="#4A5D23" opacity="0.6" r="4">
            <animate
              attributeName="r"
              dur="2s"
              repeatCount="indefinite"
              values="4;8;4"
            />
            <animate
              attributeName="opacity"
              dur="2s"
              repeatCount="indefinite"
              values="0.8;0.2;0.8"
            />
          </circle>
          <circle cx="40" cy="100" fill="#4A5D23" r="3.5" />

          {/* Pulse at Destination */}
          <circle cx="160" cy="100" fill="#4A5D23" opacity="0.6" r="4">
            <animate
              attributeName="r"
              dur="2s"
              repeatCount="indefinite"
              values="4;8;4"
            />
            <animate
              attributeName="opacity"
              dur="2s"
              repeatCount="indefinite"
              values="0.8;0.2;0.8"
            />
          </circle>
          <circle cx="160" cy="100" fill="#4A5D23" r="3.5" />
        </svg>
      </div>

      {/* Narrative Status Headline */}
      <h3 className="font-headline text-2xl md:text-[28px] font-medium text-primary mb-2.5 tracking-tight">
        Planning your journey...
      </h3>
      <p className="font-sans text-sm md:text-base text-secondary max-w-md">
        Curating scenic routes, cultural landmarks, culinary discoveries, and building your personalized itinerary.
      </p>
    </div>
  );
};
