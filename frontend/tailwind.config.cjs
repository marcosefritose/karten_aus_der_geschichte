/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'gag-primary': '#d19000',
        'gag-light': '#ffff7f'
      },
      strokeWidth: {
        '3': '3px',
        '4': '4px',
        '5': '5px',
      }
    },
  },
  safelist: ['stroke-gag-primary', 'fill-gag-primary'],
  plugins: [
    require('tailwind-scrollbar'),
  ],
}
