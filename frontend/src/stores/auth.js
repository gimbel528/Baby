import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password })
      setToken(response.data.access_token)
      await fetchUser()
      return { success: true }
    } catch (error) {
      if (!error.response) {
        return {
          success: false,
          message: `无法连接后端（${api.defaults.baseURL}）。请在 Cloudflare 配置 VITE_API_URL 后重新构建部署`
        }
      }
      const detail = error.response?.data?.detail
      return {
        success: false,
        message: typeof detail === 'string' ? detail : JSON.stringify(detail) || '登录失败'
      }
    }
  }

  const register = async (email, username, password) => {
    try {
      await api.post('/auth/register', { email, username, password })
      return { success: true }
    } catch (error) {
      if (!error.response) {
        return {
          success: false,
          message: `无法连接后端（${api.defaults.baseURL}）。请在 Cloudflare 配置 VITE_API_URL 后重新构建部署`
        }
      }
      const detail = error.response?.data?.detail
      return {
        success: false,
        message: typeof detail === 'string' ? detail : JSON.stringify(detail) || '注册失败'
      }
    }
  }

  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setToken(null)
      user.value = null
    }
  }

  const fetchUser = async () => {
    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch {
      setToken(null)
      user.value = null
    }
  }

  if (token.value) {
    fetchUser()
  }

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    login,
    register,
    logout,
    fetchUser
  }
})
