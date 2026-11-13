import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load env vars including BACKEND_PORT from the environment
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        // Proxy /api requests to the backend
        // No rewrite: backend mounts routes under /api/v1
        '/api': {
          target: `http://127.0.0.1:${env.BACKEND_PORT || 9000}`,
          changeOrigin: true,
        },
      },
    },
  }
})
