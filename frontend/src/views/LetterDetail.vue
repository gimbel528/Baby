<template>
  <div class="min-h-screen p-4 md:p-8 letter-detail-page">
    <div class="floating-bg">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
    </div>
    
    <div class="max-w-4xl mx-auto relative z-10">
      <header class="mb-8">
        <router-link to="/letters" class="back-link inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-all hover:translate-x-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          返回信件列表
        </router-link>
      </header>

      <div v-if="loading" class="text-center py-20">
        <div class="opening-envelope">
          <div class="envelope-opening">
            <div class="envelope-flap-opening"></div>
          </div>
        </div>
        <p class="text-gray-600 mt-8 text-lg">拆封中...</p>
      </div>

      <div v-else-if="letter" class="letter-detail-container">
        <div class="letter-card" :class="{ 'locked': !letter.is_unlocked }">
          <div class="letter-seal" v-if="!letter.is_unlocked"></div>
          
          <div class="letter-header">
            <div class="letter-decoration top-left">
              <svg viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M30 10 L40 30 L30 50 L20 30 Z" fill="url(#grad1)" opacity="0.3"/>
                <defs>
                  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#ec4899"/>
                    <stop offset="100%" style="stop-color:#f59e0b"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div class="letter-decoration top-right">
              <svg viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M30 10 L40 30 L30 50 L20 30 Z" fill="url(#grad2)" opacity="0.3"/>
                <defs>
                  <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#f59e0b"/>
                    <stop offset="100%" style="stop-color:#ec4899"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            
            <h1 class="letter-title text-gradient">{{ letter.title }}</h1>
            <div class="letter-meta flex flex-wrap justify-center gap-6 text-sm text-gray-600">
              <span class="meta-item flex items-center gap-2">
                <span class="w-1.5 h-1.5 bg-pink-400 rounded-full"></span>
                写于 {{ formatDate(letter.created_at) }}
              </span>
              <span v-if="letter.unlock_date" class="meta-item flex items-center gap-2">
                <span class="w-1.5 h-1.5 bg-purple-400 rounded-full"></span>
                解锁日期: {{ formatDate(letter.unlock_date) }}
              </span>
            </div>
          </div>

          <div v-if="!letter.is_unlocked" class="locked-content text-center py-12">
            <div class="lock-icon-wrapper">
              <div class="lock-icon">🔒</div>
              <div class="lock-glow"></div>
            </div>
            <h2 class="text-2xl font-semibold mb-3 text-gray-800">信件尚未解锁</h2>
            <p class="text-gray-600 mb-6">
              这封信将在 <span class="font-semibold text-pink-600">{{ formatDate(letter.unlock_date) }}</span> 解锁
            </p>
            <div class="countdown-display">
              <div class="countdown-number" id="countdown-days">00</div>
              <div class="countdown-label">天</div>
            </div>
          </div>

          <div v-else class="letter-content-body">
            <div class="paper-texture"></div>
            <div class="letter-text whitespace-pre-wrap text-gray-700 leading-relaxed text-lg">
              {{ letter.content }}
            </div>
          </div>

          <div class="letter-footer mt-10 pt-8 border-t border-gray-100 flex justify-between items-center">
            <div class="letter-signature">
              <div class="signature-line w-32 h-0.5 bg-gradient-to-r from-transparent via-gray-400 to-transparent"></div>
              <span class="text-sm text-gray-500 mt-2">爱你的爸爸妈妈</span>
            </div>
            <button 
              @click="handleDelete"
              class="delete-btn flex items-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-all hover:scale-105"
            >
              <span>🗑️</span>
              <span>删除</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()

const letter = ref(null)
const loading = ref(true)

const fetchLetter = async () => {
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    const response = await api.get(`/letters/${route.params.id}`)
    letter.value = response.data
  } catch (error) {
    console.error('获取信件失败:', error)
    alert('信件不存在')
    router.push('/letters')
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  return dayjs(date).format('YYYY年MM月DD日')
}

const handleDelete = async () => {
  if (!confirm('确定要删除这封信吗？此操作不可恢复。')) {
    return
  }

  try {
    await api.delete(`/letters/${route.params.id}`)
    alert('信件已删除')
    router.push('/letters')
  } catch (error) {
    console.error('删除信件失败:', error)
    alert('删除失败，请重试')
  }
}

onMounted(() => {
  fetchLetter()
})
</script>

<style scoped>
.letter-detail-page {
  background: linear-gradient(135deg, #fef3c7 0%, #fce7f3 50%, #dbeafe 100%);
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
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
  width: 350px;
  height: 350px;
  background: #f97316;
  bottom: -100px;
  left: -100px;
  animation-delay: 7s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(30px, 20px) rotate(90deg); }
  50% { transform: translate(0, 40px) rotate(180deg); }
  75% { transform: translate(-30px, 20px) rotate(270deg); }
}

.back-link {
  font-size: 0.95rem;
  font-weight: 500;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  backdrop-filter: blur(4px);
}

.opening-envelope {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.envelope-opening {
  position: relative;
  width: 150px;
  height: 100px;
  animation: envelopeAppear 1s ease;
}

@keyframes envelopeAppear {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.envelope-flap-opening {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50px;
  background: linear-gradient(135deg, #f97316, #ea580c);
  border-radius: 12px 12px 0 0;
  transform-origin: top;
  clip-path: polygon(0 0, 100% 0, 50% 100%);
  animation: flapOpen 1.5s ease-in-out infinite;
}

@keyframes flapOpen {
  0%, 100% {
    transform: rotateX(0deg);
  }
  50% {
    transform: rotateX(-150deg);
  }
}

.letter-detail-container {
  animation: fadeInScale 1s ease;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.letter-card {
  background: linear-gradient(180deg, #ffffff 0%, #fef9c3 100%);
  border-radius: 24px;
  padding: 50px;
  position: relative;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.8);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.letter-card.locked {
  filter: brightness(0.95);
}

.letter-seal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 140px;
  height: 140px;
  background: radial-gradient(circle at 30% 30%, #fbbf24, #f97316);
  border-radius: 50%;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 56px;
  box-shadow: 0 15px 50px rgba(249, 115, 22, 0.4), inset 0 4px 0 rgba(255, 255, 255, 0.4);
  animation: sealPulse 2s ease-in-out infinite;
}

@keyframes sealPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.08); }
}

.letter-decoration {
  position: absolute;
  width: 70px;
  height: 70px;
  opacity: 0.5;
}

.top-left {
  top: 25px;
  left: 25px;
  animation: floatSlow 6s ease-in-out infinite;
}

.top-right {
  top: 25px;
  right: 25px;
  animation: floatSlow 6s ease-in-out infinite reverse;
}

@keyframes floatSlow {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-12px) rotate(5deg); }
}

.letter-header {
  text-align: center;
  margin-bottom: 45px;
  position: relative;
  z-index: 1;
}

.letter-title {
  font-size: 2.75rem;
  margin-bottom: 24px;
  animation: slideDown 0.8s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-25px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.meta-item {
  transition: all 0.3s ease;
}

.meta-item:hover {
  transform: scale(1.05);
}

.locked-content {
  position: relative;
  z-index: 1;
}

.lock-icon-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 24px;
}

.lock-icon {
  font-size: 80px;
  animation: lockFloat 3s ease-in-out infinite;
  position: relative;
  z-index: 2;
}

@keyframes lockFloat {
  0%, 100% { transform: translateY(0) rotate(-5deg); }
  50% { transform: translateY(-18px) rotate(5deg); }
}

.lock-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 140px;
  height: 140px;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.35), transparent);
  border-radius: 50%;
  animation: glowPulse 2s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.4); opacity: 0.85; }
}

.countdown-display {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 16px 30px;
  background: linear-gradient(135deg, #ec4899, #f97316);
  border-radius: 16px;
  color: white;
  font-weight: bold;
  box-shadow: 0 6px 25px rgba(236, 72, 153, 0.35);
}

.countdown-number {
  font-size: 2.25rem;
  font-family: 'Courier New', monospace;
}

.countdown-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

.letter-content-body {
  position: relative;
  padding: 35px 0;
  animation: fadeInUp 0.9s ease 0.4s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.paper-texture {
  position: absolute;
  top: 0;
  left: -30px;
  right: -30px;
  bottom: 0;
  background-image: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 32px,
    rgba(236, 72, 153, 0.05) 32px,
    rgba(236, 72, 153, 0.05) 33px
  );
  pointer-events: none;
  z-index: 0;
}

.letter-text {
  position: relative;
  z-index: 1;
  line-height: 2.1;
  font-family: 'Georgia', 'Microsoft YaHei', serif;
  padding: 0 25px;
}

.letter-footer {
  position: relative;
  z-index: 1;
}

.signature-line {
  margin-bottom: 10px;
}

.delete-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.delete-btn:hover {
  background: #fee2e2;
  transform: scale(1.05);
}

.delete-btn:active {
  transform: scale(0.98);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .letter-card {
    padding: 30px 24px;
  }
  
  .letter-title {
    font-size: 2rem;
  }
  
  .letter-decoration {
    width: 45px;
    height: 45px;
  }
  
  .lock-icon {
    font-size: 56px;
  }
  
  .countdown-display {
    padding: 12px 22px;
  }
  
  .countdown-number {
    font-size: 1.75rem;
  }
}
</style>
