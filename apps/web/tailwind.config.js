/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#1A1A1A',
        'primary-container': '#1C1B1B',
        'on-primary': '#FFFFFF',
        'on-primary-container': '#858383',
        'primary-fixed': '#E5E2E1',
        'primary-fixed-dim': '#C8C6C5',
        'on-primary-fixed': '#1C1B1B',
        'on-primary-fixed-variant': '#474746',
        
        secondary: '#5E5F5D',
        'secondary-container': '#E0E0DD',
        'on-secondary': '#FFFFFF',
        'on-secondary-container': '#626361',
        'secondary-fixed': '#E3E2E0',
        'secondary-fixed-dim': '#C7C6C4',
        'on-secondary-fixed': '#1A1C1A',
        'on-secondary-fixed-variant': '#464745',

        tertiary: '#000000',
        'tertiary-container': '#062014',
        'on-tertiary': '#FFFFFF',
        'on-tertiary-container': '#6E8A79',
        'tertiary-fixed': '#CCEAD6',
        'tertiary-fixed-dim': '#B0CDBB',
        'on-tertiary-fixed': '#062014',
        'on-tertiary-fixed-variant': '#324C3E',

        background: '#FAF9F6',
        'on-background': '#1C1B1B',
        
        surface: '#FDF8F8',
        'surface-dim': '#DDD9D8',
        'surface-bright': '#FDF8F8',
        'surface-container-lowest': '#FFFFFF',
        'surface-container-low': '#F7F3F2',
        'surface-container': '#F1EDEC',
        'surface-container-high': '#EBE7E6',
        'surface-container-highest': '#E5E2E1',
        'on-surface': '#1C1B1B',
        'on-surface-variant': '#444748',
        'inverse-surface': '#313030',
        'inverse-on-surface': '#F4F0EF',
        'surface-tint': '#5F5E5E',
        'surface-variant': '#E5E2E1',

        outline: '#747878',
        'outline-variant': '#C4C7C7',

        error: '#BA1A1A',
        'on-error': '#FFFFFF',
        'error-container': '#FFDAD6',
        'on-error-container': '#93000A',

        // Brand Accents
        sand: '#D9C5B2',
        terracotta: '#CC4F36',
        'terracotta-dark': '#A0522D',
        'earthy-green': '#4A5D23',
        'earthy-green-dark': '#2D4739',
        ivory: '#FAF9F6',
      },
      borderRadius: {
        DEFAULT: '0.25rem', // 4px
        sm: '0.125rem',     // 2px
        md: '0.375rem',     // 6px
        lg: '0.5rem',       // 8px
        xl: '0.75rem',      // 12px
        full: '9999px',
      },
      spacing: {
        'margin-mobile': '20px',
        'margin-desktop': '80px',
        gutter: '24px',
        'section-gap': '64px',
        unit: '8px',
      },
      fontFamily: {
        headline: ['"Playfair Display"', 'Georgia', 'serif'],
        display: ['"Playfair Display"', 'Georgia', 'serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display-lg': ['64px', { lineHeight: '72px', letterSpacing: '-0.02em', fontWeight: '700' }],
        'headline-lg': ['40px', { lineHeight: '48px', fontWeight: '600' }],
        'headline-lg-mobile': ['32px', { lineHeight: '40px', fontWeight: '600' }],
        'headline-md': ['28px', { lineHeight: '36px', fontWeight: '500' }],
        'headline-sm': ['22px', { lineHeight: '28px', fontWeight: '500' }],
        'body-lg': ['18px', { lineHeight: '28px', fontWeight: '400' }],
        'body-md': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'body-sm': ['14px', { lineHeight: '20px', fontWeight: '400' }],
        'ui-button': ['14px', { lineHeight: '20px', fontWeight: '500' }],
        'label-caps': ['12px', { lineHeight: '16px', letterSpacing: '0.1em', fontWeight: '600' }],
      },
      boxShadow: {
        subtle: '0 4px 20px -2px rgba(28, 27, 27, 0.04)',
        editorial: '0 20px 40px -15px rgba(45, 71, 57, 0.08)',
      },
    },
  },
  plugins: [],
};
