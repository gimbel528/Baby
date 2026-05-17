<template>
  <div class="fixed inset-0 flex items-center justify-center z-50 p-4">
    <div class="backdrop absolute inset-0" @click="handleClose"></div>
    
    <div class="modal-content relative max-w-lg w-full">
      <div class="modal-decoration top-decoration"></div>
      
      <button @click="handleClose" class="close-btn absolute top-6 right-6 w-10 h-10 rounded-full bg-white/80 flex items-center justify-center hover:bg-white transition-all hover:scale-110 z-10">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>

      <div class="modal-header text-center mb-8 pt-8">
        <div class="icon-wrapper inline-block mb-4">
          <span class="text-4xl">⏰</span>
        </div>
        <h2 class="text-2xl md:text-3xl font-bold text-gradient">添加倒计时事件</h2>
        <p class="text-gray-600 mt-2">记录一个重要的日子</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="form-field">
          <label class="field-label flex items-center gap-2">
            <span class="text-lg">📝</span>
            事件名称
          </label>
          <input 
            v-model="form.event_name"
            type="text"
            required
            class="form-input"
            placeholder="例如：宝宝的预产期"
          />
        </div>

        <div class="form-field">
          <label class="field-label flex items-center gap-2">
            <span class="text-lg">📅</span>
            目标日期
          </label>
          <input 
            v-model="form.target_date"
            type="date"
            required
            class="form-input"
          />
        </div>

        <div class="form-field">
          <label class="field-label flex items-center gap-2">
            <span class="text-lg">🎨</span>
            事件类型
          </label>
          <div class="type-grid">
            <button 
              v-for="type in eventTypes" 
              :key="type.value"
              type="button"
              @click="selectEventType(type.value)"
              class="type-btn"
              :class="{ active: form.event_type === type.value }"
            >
              <span class="text-2xl mb-2">{{ type.icon }}</span>
              <span class="text-sm font-medium">{{ type.label }}</span>
            </button>
          </div>
        </div>

        <div class="button-group flex gap-4 pt-4">
          <button type="button" @click="handleClose" class="btn-cancel flex-1">
            取消
          </button>
          <button type="submit" class="btn-submit flex-1" :disabled="loading">
            <span v-if="loading" class="flex items-center justify-center gap-2">
              <span class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              添加中...
            </span>
            <span v-else class="flex items-center justify-center gap-2">
              <span>✨</span>
              添加事件
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const emit = defineEmits(['close', 'added'])

const eventTypes = [
  { value: 'birth', label: '预产期', icon: '🤰' },
  { value: 'birthday', label: '生日', icon: '🎂' },
  { value: 'milestone', label: '里程碑', icon: '🌟' },
  { value: 'custom', label: '自定义', icon: '💖' }
]

const form = ref({
  event_name: '',
  target_date: '',
  event_type: 'birth'
})

const loading = ref(false)

const selectEventType = (value) => {
  console.log('选择事件类型:', value)
  form.value.event_type = value
}

const handleClose = () => {
  emit('close')
}

const handleSubmit = async () => {
  console.log('提交表单:', form.value)
  
  if (!form.value.event_name || !form.value.target_date) {
    alert('请填写完整信息')
    return
  }
  
  loading.value = true
  
  try {
    const targetDate = new Date(form.value.target_date + 'T00:00:00')
    const data = {
      event_name: form.value.event_name,
      target_date: targetDate.toISOString(),
      event_type: form.value.event_type
    }
    
    console.log('发送数据:', data)
    const response = await api.post('/countdown/', data)
    console.log('响应数据:', response.data)
    
    alert('添加成功！')
    
    // 重置表单
    form.value = {
      event_name: '',
      target_date: '',
      event_type: 'birth'
    }
    
    emit('added')
  } catch (error) {
    console.error('添加事件失败:', error)
    if (error.response) {
      console.error('错误响应:', error.response.data)
    }
    alert(`添加失败: ${error.response?.data?.detail || error.message || '请重试'}`)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.backdrop {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.3), rgba(236, 72, 153, 0.3));
  backdrop-filter: blur(8px);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: linear-gradient(180deg, #ffffff 0%, #fef3c7 100%);
  border-radius: 32px;
  padding: 48px 40px 40px;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.8);
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-decoration {
  position: absolute;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  opacity: 0.1;
  animation: float 6s ease-in-out infinite;
}

.top-decoration {
  top: -100px;
  right: -50px;
  background: linear-gradient(135deg, #ec4899, #f97316);
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.icon-wrapper {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #fef3c7, #fce7f3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 30px rgba(236, 72, 153, 0.2), inset 0 2px 0 rgba(255, 255, 255, 0.8);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.form-field {
  position: relative;
}

.field-label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 10px;
  font-size: 0.95rem;
}

.form-input {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
}

.form-input:focus {
  border-color: #ec4899;
  box-shadow: 0 0 0 4px rgba(236, 72, 153, 0.1), 0 4px 20px rgba(236, 72, 153, 0.15);
  transform: translateY(-2px);
}

.type-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px 10px;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.type-btn:hover {
  border-color: #f97316;
  background: rgba(254, 243, 199, 0.5);
  transform: translateY(-2px);
}

.type-btn.active {
  border-color: #ec4899;
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(249, 115, 22, 0.1));
  box-shadow: 0 4px 20px rgba(236, 72, 153, 0.2);
  transform: scale(1.02);
}

.button-group {
  margin-top: 8px;
}

.btn-cancel {
  padding: 14px 24px;
  border-radius: 14px;
  border: 2px solid #e5e7eb;
  background: white;
  color: #4b5563;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-cancel:hover {
  border-color: #9ca3af;
  background: #f9fafb;
  transform: translateY(-2px);
}

.btn-submit {
  padding: 14px 24px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #ec4899, #f97316);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(236, 72, 153, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(236, 72, 153, 0.4);
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .modal-content {
    padding: 36px 24px 28px;
    border-radius: 24px;
  }
  
  .type-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
