import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api': {  // 使用 /api 前缀进行代理
        target: 'http://127.0.0.1:8080',  // 指向后端的地址和端口
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
    }
})
