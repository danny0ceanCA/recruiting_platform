/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primaryDark: '#112240',
        circuitBlue: '#073642',
      },
    },
  },
  plugins: [],
}
