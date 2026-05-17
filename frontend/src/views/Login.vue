<template>
  <div style="max-width:400px;margin:50px auto;padding:20px">
    <h2>{{ isLogin ? "登录" : "注册" }}</h2>
    
    <input 
      v-model="email" 
      placeholder="邮箱"
      style="width:100%;margin:10px 0;padding:10px"
    />
    <input 
      v-model="password" 
      type="password"
      placeholder="密码"
      style="width:100%;margin:10px 0;padding:10px"
    />

    <button 
      @click="submit"
      style="width:100%;padding:10px;background:#4f46e5;color:white;border:none;border-radius:5px"
    >
      {{ isLogin ? "登录" : "注册" }}
    </button>

    <p style="text-align:center;margin-top:10px">
      <a @click="isLogin = !isLogin" style="color:#4f46e5;cursor:pointer">
        {{ isLogin ? "去注册" : "去登录" }}
      </a>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { supabase } from '@/supabase'

const email = ref('')
const password = ref('')
const isLogin = ref(true)

// 登录 / 注册 提交
const submit = async () => {
  if (isLogin.value) {
    // 登录
    const { error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value
    })
    if (error) alert(error.message)
    else alert("登录成功！🎉")
  } else {
    // 注册
    const { error } = await supabase.auth.signUp({
      email: email.value,
      password: password.value
    })
    if (error) alert(error.message)
    else alert("注册成功！请到邮箱验证 ✅")
  }
}
</script>