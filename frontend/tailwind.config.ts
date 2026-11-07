import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './composables/**/*.{js,ts}',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      colors: {
        wood: {
          50: '#fdf8f0',
          100: '#f9eee0',
          200: '#f2dac1',
          300: '#e8c09a',
          400: '#db9d6d',
          500: '#cb7a46',
          600: '#b85f36',
          700: '#96482c',
          800: '#7a3b29',
          900: '#643224',
          950: '#381810',
        },
        guitar: {
          amber: '#f59e0b',
          cedar: '#c2410c',
          spruce: '#fef3c7',
          rosewood: '#451a03',
          ebony: '#0d0f12',
          brass: '#eab308',
        },
        studio: {
          dark: '#0a0c10',
          card: '#12161f',
          border: '#1e2433',
          muted: '#8b9bb4',
        }
      },
      fontFamily: {
        sans: ['Vazirmatn', 'Shabnam', 'Tahoma', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      animation: {
        'wave-bar': 'waveBar 1.2s ease-in-out infinite alternate',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        waveBar: {
          '0%': { height: '15%' },
          '100%': { height: '100%' },
        }
      }
    },
  },
  plugins: [],
} satisfies Config
