import axios from 'axios'

// 本地开发走 vite proxy 的 /api；生产优先用 Cloudflare 构建变量 VITE_API_URL
const RAILWAY_API = 'https://baby-production-6e69.up.railway.app/api'
const baseURL =
  import.meta.env.VITE_API_URL ||
  (import.meta.env.PROD ? RAILWAY_API : '/api')

if (import.meta.env.PROD && !import.meta.env.VITE_API_URL) {
  console.warn(
    '[api] 未检测到 VITE_API_URL，使用默认 Railway 地址。建议在 Cloudflare 配置该变量后重新构建。'
  )
}

const api = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
