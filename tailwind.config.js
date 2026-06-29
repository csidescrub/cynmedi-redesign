/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.html',
    './work/*.html',
    './aesthetic-clinic/*.html',
    './dental-clinic/*.html',
    './lp/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Kanit', 'Inter', 'system-ui', 'sans-serif'],
        display: ['Cormorant Garamond', 'Kanit', 'sans-serif'],
      },
      colors: {
        ink: {
          50: '#F7F8FB',
          100: '#EEF1F6',
          200: '#D9DFE9',
          300: '#B4BECF',
          400: '#7F8DA8',
          500: '#536685',
          600: '#384962',
          700: '#1F2D44',
          800: '#0F1B30',
          900: '#070F1E',
        },
        royal: {
          100: '#E8EDF8',
          200: '#C7D2EE',
          300: '#94A6DB',
          400: '#5A75C5',
          500: '#3554B3',
          600: '#2C4CAA',
          700: '#23408F',
          800: '#1B3375',
          900: '#15295E',
        },
        cobalt: '#2D4DB1',
      },
    },
  },
  plugins: [],
};
