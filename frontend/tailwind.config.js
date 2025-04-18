/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif'],
      },
      colors: {
        // Color Scheme 1 - Base colors
        'royal-blue': {
          light: '#D7DDFB',
          DEFAULT: '#4758DC',
          dark: '#3A46B0',
        },
        'ice-cold': {
          light: '#E0F1FF',
          DEFAULT: '#A5D8FF',
          dark: '#78A9D8',
        },
        // Color Scheme 3 - Neutrals
        'neutral': {
          lighter: '#F7F7F7',
          light: '#E5E5E5',
          DEFAULT: '#B3B3B3',
          dark: '#717171',
          darker: '#191919',
        },
        // Input borders
        'input-border': '#D8DBE8',
      },
      borderRadius: {
        'sm': '0.25rem',
        'md': '0.5rem',
        'lg': '1rem',
        'xl': '1.5rem',
      },
      boxShadow: {
        'small': '0 2px 5px rgba(0, 0, 0, 0.05)',
        'medium': '0 4px 10px rgba(0, 0, 0, 0.08)',
        'large': '0 10px 20px rgba(0, 0, 0, 0.12)',
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.5s ease-out forwards',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        qontrolla: {
          "primary": "#4758DC",
          "secondary": "#A5D8FF",
          "accent": "#37CDBE",
          "neutral": "#191919",
          "base-100": "#FFFFFF",
          "info": "#3ABFF8",
          "success": "#36D399",
          "warning": "#FBBD23",
          "error": "#F87272",
        },
      },
    ],
  },
} 