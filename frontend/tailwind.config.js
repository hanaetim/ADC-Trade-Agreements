/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg': '#F2F5F8',
        'surface': '#FFFFFF',
        'surface-alt': '#F8FAFC',
        'border': '#CBD3DC',
        'border-strong': '#8C99A6',
        'text': '#17222D',
        'text-muted': '#4A5866',
        'primary': '#12405E',
        'primary-contrast': '#FFFFFF',
        'primary-soft': '#E3EDF5',
        'focus': '#0A5CAD',
        'success-fg': '#16602F',
        'success-bg': '#E1F2E6',
        'danger-fg': '#9B1C1C',
        'danger-bg': '#FBE4E4',
        'warning-fg': '#6F4300',
        'warning-bg': '#FFEFCC',
        'info-fg': '#14507F',
        'info-bg': '#E0EDF8',
        'neutral-fg': '#36424E',
        'neutral-bg': '#E6EAEE',
        'future-fg': '#56626E',
      },
      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '24px',
        '6': '32px',
        '7': '48px',
      },
      borderRadius: {
        'sm': '4px',
        'md': '8px',
      },
      fontFamily: {
        'sans': ['system-ui', '-apple-system', '"Segoe UI"', 'Roboto', '"Noto Sans"', '"Helvetica Neue"', 'sans-serif'],
        'mono': ['ui-monospace', '"SF Mono"', 'Consolas', '"Liberation Mono"', 'Menlo', 'monospace'],
      },
    },
  },
  plugins: [],
}
