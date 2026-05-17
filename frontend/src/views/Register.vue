<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="card max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-display font-bold text-gradient mb-2">
          创建账户
        </h1>
        <p class="text-gray-600">开始记录宝宝的成长</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
          <input 
            v-model="form.username"
            type="text"
            required
            class="input-field"
            placeholder="您的昵称"
          />
        </div>

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
            placeholder="至少8个字符"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">确认密码</label>
          <input 
            v-model="form.confirmPassword"
            type="password"
            required
            class="input-field"
            placeholder="再次输入密码"
          />
        </div>

        <div v-if="error" class="text-red-500 text-sm text-center">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-600">
          已有账户？
          <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">
            立即登录
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
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    error.value = '两次输入的密码不一致'
    return
  }

  if (form.value.password.length < 8) {
    error.value = '密码至少需要8个字符'
    return
  }

  loading.value = true
  error.value = ''
  
  const result = await authStore.register(
    form.value.email,
    form.value.username,
    form.value.password
  )
  
  if (result.success) {
    alert('注册成功！请登录')
    router.push('/login')
  } else {
    error.value = result.message
  }
  
  loading.value = false
}
</script>
