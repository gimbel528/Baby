import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  
  const isAuthenticated = computed(() => !!token.value)
  
  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
    } else {
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
  
  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/auth/login', { email, password })
      setToken(response.data.access_token)
      await fetchUser()
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '登录失败' 
      }
    }
  }
  
  const register = async (email, username, password) => {
    try {
      await axios.post('/api/auth/register', { email, username, password })
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '注册失败' 
      }
    }
  }
  
  const logout = async () => {
    try {
      await axios.post('/api/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setToken(null)
      user.value = null
    }
  }
  
  const fetchUser = async () => {
    try {
      const response = await axios.get('/api/auth/me')
      user.value = response.data
    } catch (error) {
      setToken(null)
    }
  }
  
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    fetchUser()
  }
  
  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
})
