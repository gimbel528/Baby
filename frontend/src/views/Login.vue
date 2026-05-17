<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="card max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-display font-bold text-gradient mb-2">
          欢迎回来
        </h1>
        <p class="text-gray-600">登录您的账户</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
          <input 
            v-model="form.email"
            type="email"
            required
            class="input-field"
            placeholder="your@email.com"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
          <input 
            v-model="form.password"
            type="password"
            required
            class="input-field"
            placeholder="••••••••"
          />
        </div>

        <div v-if="error" class="text-red-500 text-sm text-center">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-600">
          还没有账户？
          <router-link to="/register" class="text-primary-600 hover:text-primary-700 font-medium">
            立即注册
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  const result = await authStore.login(form.value.email, form.value.password)
  
  if (result.success) {
    router.push('/')
  } else {
    error.value = result.message
  }
  
  loading.value = false
}
</script>
