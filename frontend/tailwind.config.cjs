/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      screens: {
        '2xl': '1900px'
      },
      colors: {
        'gag-primary': '#d19000',
        'gag-light': '#ffff7f'
      },
      strokeWidth: {
        '3': '3px',
        '4': '4px',
        '5': '5px',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite'
      },
      keyframes: {
        pulse: {
          '0%, 100%' : {opacity: 1, transform: 'scale(2.5)'},
          '50%': { opacity: .6, transform: 'scale(1.75)' }
        }
      }
    },
  },
  safelist: ['stroke-gag-primary', 'fill-gag-primary'],
  plugins: [
    require('tailwind-scrollbar'),
  ],
}
