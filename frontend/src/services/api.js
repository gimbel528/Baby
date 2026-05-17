import axios from 'axios'

/** 生产后端（Railway） */
export const RAILWAY_API = 'https://baby-production-6e69.up.railway.app/api'

function resolveApiBaseURL() {
  const raw = import.meta.env.VITE_API_URL?.trim()

  // 必须是完整 https 地址；/api 或 api 这类相对路径会导致 405（打到 Cloudflare 静态站）
  if (raw && /^https?:\/\//i.test(raw)) {
    try {
      const parsed = new URL(raw)
      if (typeof window !== 'undefined' && parsed.origin === window.location.origin) {
        console.error(
          '[api] VITE_API_URL 不能填前端自己的域名，请改为 Railway 地址:',
          RAILWAY_API
        )
        return RAILWAY_API
      }
      return raw.replace(/\/$/, '')
    } catch {
      /* 非法 URL，走下方回退 */
    }
  } else if (raw && import.meta.env.PROD) {
    console.error(
      '[api] VITE_API_URL 格式错误（当前值无效），应类似:',
      RAILWAY_API,
      '实际:',
      raw
    )
  }

  if (import.meta.env.DEV) {
    return '/api'
  }
  return RAILWAY_API
}

export const apiBaseURL = resolveApiBaseURL()

if (import.meta.env.PROD) {
  console.info('[api] baseURL =', apiBaseURL)
}

const api = axios.create({
  baseURL: apiBaseURL,
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
  (error) => Promise.reject(error)
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
