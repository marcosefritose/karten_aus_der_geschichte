/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      fontFamily: {
        classicalHumanist: ['Optima', 'Candara', 'Noto Sans', 'source-sans-pro', 'sans-serif'],
        geometricHumanist: ['Avenir', 'Avenir Next LT Pro', 'Montserrat', 'Corbel', 'URW Gothic', 'source-sans-pro', 'sans-serif'],
        transitional: ['Charter', 'Bitstream Charter', 'Sitka Text', 'Cambria', 'serif'],
        oldStyle: ['Iowan Old Style', 'Palatino Linotype', 'URW Palladio L', 'P052', 'serif']

      },
      screens: {
        '2xl': '1900px'
      },
      colors: {
        'gag-primary': '#d19000',
        'gag-secondary': '#ffff7f',
        'gag-light': '#FFEFD1',
        'gag-white': '#FFF9F9',
        'active': '#1BAA04',
        'active-light': '#C8FFBF',
        'pending': '#A7AA04',
        'pending-light': '#F3FFA7',
        'hidden': '#AA0404',
        'hidden-light': '#FFBFBF',
      },
      strokeWidth: {
        '3': '3px',
        '4': '4px',
        '5': '5px',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite'
      },
      keyframes: {
        pulse: {
          '0%, 100%': { opacity: .9, transform: 'scale(2.5)' },
          '50%': { opacity: .6, transform: 'scale(1.75)' }
        }
      },

    },
  },
  safelist: ['stroke-gag-primary', 'fill-gag-primary', 'text-active', 'text-pending', 'text-hidden', 'bg-active-light', 'bg-pending-light', 'bg-hidden-light', 'fill-active-light', 'fill-hidden-light'],
  plugins: [
    require('tailwind-scrollbar'),
  ],
}
