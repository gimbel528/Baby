<template>
  <div class="max-w-md mx-auto mt-16 p-6">
    <h2 class="text-2xl font-bold text-center mb-6">
      {{ isLogin ? '登录' : '注册' }}
    </h2>

    <input
      v-model="email"
      type="email"
      placeholder="邮箱"
      class="input-field mb-3"
    />
    <input
      v-if="!isLogin"
      v-model="username"
      type="text"
      placeholder="昵称"
      class="input-field mb-3"
    />
    <input
      v-model="password"
      type="password"
      placeholder="密码"
      class="input-field mb-4"
    />

    <p v-if="error" class="text-red-600 text-sm mb-3">{{ error }}</p>

    <button
      type="button"
      class="btn-primary w-full"
      :disabled="loading"
      @click="submit"
    >
      {{ loading ? '请稍候...' : isLogin ? '登录' : '注册' }}
    </button>

    <p class="text-center mt-4 text-gray-600">
      <button type="button" class="text-primary-600" @click="toggleMode">
        {{ isLogin ? '去注册' : '去登录' }}
      </button>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const password = ref('')
const isLogin = ref(true)
const loading = ref(false)
const error = ref('')

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
}

const submit = async () => {
  error.value = ''
  loading.value = true

  try {
    if (isLogin.value) {
      const result = await authStore.login(email.value, password.value)
      if (result.success) {
        router.push('/')
      } else {
        error.value = result.message
      }
    } else {
      if (!username.value.trim()) {
        error.value = '请填写昵称'
        return
      }
      if (password.value.length < 8) {
        error.value = '密码至少 8 位'
        return
      }
      const result = await authStore.register(
        email.value,
        username.value.trim(),
        password.value
      )
      if (result.success) {
        alert('注册成功，请登录')
        isLogin.value = true
      } else {
        error.value = result.message
      }
    }
  } finally {
    loading.value = false
  }
}
</script>
