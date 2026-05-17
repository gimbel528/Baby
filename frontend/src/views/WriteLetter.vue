<template>
  <div class="min-h-screen py-8 px-4 write-page">
    <div class="floating-bg">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
    </div>
    
    <div class="max-w-5xl mx-auto relative z-10">
      <div class="mb-8">
        <router-link to="/letters" class="back-btn inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-all hover:translate-x-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          返回信件列表
        </router-link>
      </div>

      <div class="page-header text-center mb-10">
        <div class="header-icon inline-block mb-4">
          <span class="text-5xl">💌</span>
        </div>
        <h1 class="text-3xl md:text-4xl font-bold text-gradient mb-2">写一封信</h1>
        <p class="text-gray-600 text-lg">把您的爱和期待写下来</p>
      </div>

      <form @submit.prevent="handleSubmit" class="letter-form">
        <div class="paper-card">
          <div class="paper-texture"></div>
          
          <div class="form-section mb-8">
            <label class="form-label flex items-center gap-3">
              <span class="text-2xl">📖</span>
              信件标题
            </label>
            <input 
              v-model="form.title"
              type="text"
              required
              class="form-input-title"
              placeholder="给宝宝的第一封信..."
            />
          </div>

          <div class="form-section mb-8">
            <label class="form-label flex items-center gap-3">
              <span class="text-2xl">✍️</span>
              信件内容
            </label>
            <textarea 
              v-model="form.content"
              required
              class="form-input-content"
              placeholder="亲爱的宝贝，我想对你说..."
            ></textarea>
          </div>

          <div class="options-section">
            <h3 class="options-title flex items-center gap-2 mb-6">
              <span class="text-xl">⚙️</span>
              更多选项
            </h3>
            
            <div class="options-grid">
              <div class="option-item">
                <label class="option-label">
                  <span class="option-icon">🔓</span>
                  解锁日期
                </label>
                <input 
                  v-model="form.unlock_date"
                  type="date"
                  class="option-input"
                />
                <p class="option-hint">留空则立即解锁</p>
              </div>

              <div class="option-item">
                <label class="option-label">
                  <span class="option-icon">🔔</span>
                  提醒日期
                </label>
                <input 
                  v-model="form.reminder_date"
                  type="date"
                  class="option-input"
                />
                <p class="option-hint">在指定日期提醒您</p>
              </div>
            </div>
          </div>
        </div>

        <div class="action-buttons flex gap-4 pt-8">
          <router-link to="/letters" class="btn-cancel flex-1 flex items-center justify-center gap-2">
            <span>❌</span>
            取消
          </router-link>
          <button type="submit" class="btn-save flex-1 flex items-center justify-center gap-2" :disabled="loading">
            <span v-if="loading" class="flex items-center gap-2">
              <span class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              保存中...
            </span>
            <span v-else class="flex items-center gap-2">
              <span>✨</span>
              保存信件
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()

const form = ref({
  title: '',
  content: '',
  unlock_date: '',
  reminder_date: ''
})

const loading = ref(false)

const handleSubmit = async () => {
  console.log('提交信件表单:', form.value)
  
  if (!form.value.title || !form.value.content) {
    alert('请填写信件标题和内容')
    return
  }
  
  loading.value = true
  
  try {
    const data = {
      title: form.value.title,
      content: form.value.content
    }
    
    if (form.value.unlock_date) {
      const unlockDate = new Date(form.value.unlock_date + 'T00:00:00')
      data.unlock_date = unlockDate.toISOString()
    }
    
    if (form.value.reminder_date) {
      const reminderDate = new Date(form.value.reminder_date + 'T00:00:00')
      data.reminder_date = reminderDate.toISOString()
    }
    
    console.log('发送信件数据:', data)
    
    await api.post('/letters/', data)
    
    console.log('信件保存成功')
    alert('信件保存成功！💌')
    router.push('/letters')
  } catch (error) {
    console.error('保存信件失败:', error)
    if (error.response) {
      console.error('错误响应:', error.response.data)
    }
    alert(`保存失败: ${error.response?.data?.detail || error.message || '请重试'}`)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.write-page {
  background: linear-gradient(135deg, #fef3c7 0%, #fce7f3 50%, #dbeafe 100%);
  min-height: 100vh;
  position: relative;
}

.floating-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 0;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
  animation: float 20s ease-in-out infinite;
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: #ec4899;
  top: -150px;
  right: -150px;
  animation-delay: 0s;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #3b82f6;
  bottom: -100px;
  left: -100px;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(50px, 30px) rotate(90deg); }
  50% { transform: translate(0, 60px) rotate(180deg); }
  75% { transform: translate(-50px, 30px) rotate(270deg); }
}

.back-btn {
  font-size: 0.95rem;
  font-weight: 500;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  backdrop-filter: blur(4px);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.95);
}

.header-icon {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, #fef3c7, #fce7f3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 40px rgba(236, 72, 153, 0.2), inset 0 4px 0 rgba(255, 255, 255, 0.8);
  animation: bounce 3s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.letter-form {
  position: relative;
}

.paper-card {
  background: linear-gradient(180deg, #ffffff 0%, #fef9c3 100%);
  border-radius: 32px;
  padding: 48px;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
}

.paper-texture {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 35px,
    rgba(236, 72, 153, 0.03) 35px,
    rgba(236, 72, 153, 0.03) 36px
  );
  pointer-events: none;
  z-index: 0;
}

.form-section {
  position: relative;
  z-index: 1;
}

.form-label {
  display: block;
  font-weight: 700;
  color: #374151;
  margin-bottom: 14px;
  font-size: 1.05rem;
}

.form-input-title {
  width: 100%;
  padding: 18px 22px;
  border: 2px solid #e5e7eb;
  border-radius: 18px;
  font-size: 1.15rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(4px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  font-weight: 600;
}

.form-input-title:focus {
  border-color: #ec4899;
  box-shadow: 0 0 0 5px rgba(236, 72, 153, 0.1), 0 6px 30px rgba(236, 72, 153, 0.15);
  transform: translateY(-2px);
}

.form-input-content {
  width: 100%;
  min-height: 380px;
  padding: 22px;
  border: 2px solid #e5e7eb;
  border-radius: 20px;
  font-size: 1.1rem;
  line-height: 1.9;
  font-family: 'Georgia', 'Microsoft YaHei', serif;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(4px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  resize: vertical;
}

.form-input-content:focus {
  border-color: #ec4899;
  box-shadow: 0 0 0 5px rgba(236, 72, 153, 0.1), 0 6px 30px rgba(236, 72, 153, 0.15);
  transform: translateY(-2px);
}

.options-section {
  position: relative;
  z-index: 1;
  padding: 28px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  border: 1px dashed rgba(236, 72, 153, 0.2);
}

.options-title {
  font-weight: 700;
  color: #4b5563;
  font-size: 1.05rem;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.option-item {
  display: flex;
  flex-direction: column;
}

.option-label {
  font-weight: 600;
  color: #374151;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.option-icon {
  font-size: 1.3rem;
}

.option-input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
}

.option-input:focus {
  border-color: #ec4899;
  box-shadow: 0 0 0 4px rgba(236, 72, 153, 0.1);
}

.option-hint {
  margin-top: 8px;
  font-size: 0.85rem;
  color: #9ca3af;
}

.action-buttons {
  margin-top: 8px;
}

.btn-cancel {
  padding: 16px 28px;
  border-radius: 16px;
  border: 2px solid #e5e7eb;
  background: rgba(255, 255, 255, 0.9);
  color: #4b5563;
  font-weight: 600;
  font-size: 1.05rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-cancel:hover {
  border-color: #9ca3af;
  background: #f9fafb;
  transform: translateY(-2px);
}

.btn-save {
  padding: 16px 28px;
  border-radius: 16px;
  border: none;
  background: linear-gradient(135deg, #ec4899, #f97316);
  color: white;
  font-weight: 600;
  font-size: 1.05rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 6px 30px rgba(236, 72, 153, 0.35);
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(236, 72, 153, 0.45);
}

.btn-save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .paper-card {
    padding: 28px 20px;
    border-radius: 24px;
  }
  
  .form-input-content {
    min-height: 280px;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>
