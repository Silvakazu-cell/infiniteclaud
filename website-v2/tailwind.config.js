/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: '#D4A843',
        cyan: '#06B6D4',
        dark: '#0F0F0F',
        'light-text': '#F5F0E8',
        'mid-text': '#A0A0A0',
        'dim-text': '#6B6B6B',
      },
    },
  },
  plugins: [],
}
