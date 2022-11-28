/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'gag-primary': '#d19000',
        'gag-light': '#ffff7f'
      }
    },
  },
  safelist: ['stroke-gag-primary', 'fill-gag-primary'],
  plugins: [],
}
