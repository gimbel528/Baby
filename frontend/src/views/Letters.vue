<template>
  <div class="min-h-screen letters-page">
    <div class="floating-bg">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-8 relative z-10">
      <header class="page-header flex flex-col md:flex-row justify-between items-center mb-12">
        <div class="header-left text-center md:text-left mb-6 md:mb-0">
          <router-link to="/" class="back-link inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-all hover:translate-x-1 mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            返回首页
          </router-link>
          
          <div class="logo-container">
            <div class="logo-icon">
              <span class="text-4xl">💌</span>
            </div>
            <h1 class="logo-text text-2xl md:text-3xl font-bold text-gradient">
              给宝宝的信
            </h1>
            <p class="logo-subtitle text-gray-600 mt-2 text-sm">
              记录每一份珍贵的爱
            </p>
          </div>
        </div>
        
        <router-link to="/write" class="write-btn flex items-center gap-2 px-6 py-3 rounded-2xl bg-gradient-to-r from-pink-500 to-orange-500 text-white font-semibold text-base shadow-lg hover:shadow-xl transition-all hover:scale-105 hover:-translate-y-1">
          <span class="text-xl">✉️</span>
          写一封信
        </router-link>
      </header>

      <div v-if="letters.length === 0" class="empty-state text-center py-20">
        <div class="empty-icon text-6xl mb-6 animate-bounce">💌</div>
        <h2 class="text-2xl font-semibold mb-4 text-gray-800">还没有信件</h2>
        <p class="text-gray-600 mb-8 text-base">写下第一封信，开始记录您的心声</p>
        <router-link to="/write" class="write-btn flex items-center gap-2 px-6 py-3 rounded-2xl bg-gradient-to-r from-pink-500 to-orange-500 text-white font-semibold text-base shadow-lg hover:shadow-xl transition-all hover:scale-105 hover:-translate-y-1 mx-auto">
          <span class="text-xl">✨</span>
          写第一封信
        </router-link>
      </div>

      <div v-else class="envelopes-grid grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <div 
          v-for="(letter, index) in letters" 
          :key="letter.id"
          class="envelope-wrapper"
          :style="{ animationDelay: `${index * 0.15}s` }"
        >
          <div class="envelope-container" @click="openLetter(letter.id)">
            <div class="envelope">
              <div class="envelope-shadow"></div>
              
              <div class="envelope-back"></div>
              
              <div class="letter-paper">
                <div class="paper-content">
                  <h3 class="paper-title font-semibold text-gray-800">{{ letter.title }}</h3>
                  <p class="paper-date text-gray-500">{{ formatDate(letter.created_at) }}</p>
                  <p class="paper-preview text-gray-600 mt-2">
                    {{ letter.is_unlocked ? (letter.content.length > 45 ? letter.content.slice(0, 45) + '...' : letter.content) : '这封信将在未来某个时刻解锁...' }}
                  </p>
                </div>
              </div>
              
              <div class="envelope-front">
                <div class="envelope-flap">
                  <div class="flap-seal"></div>
                </div>
                <div class="envelope-body">
                  <div class="stamp">💖</div>
                  <div class="envelope-label">
                    <span class="label-icon">✨</span>
                    <span class="label-text">给宝宝</span>
                  </div>
                  <div v-if="letter.unlock_date" class="unlock-date">
                    <span class="unlock-label">开启日</span> {{ formatDate(letter.unlock_date) }}
                  </div>
                  <div v-if="!letter.is_unlocked" class="lock-badge">
                    🔒
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'
import dayjs from 'dayjs'

const router = useRouter()
const letters = ref([])

const fetchLetters = async () => {
  try {
    const response = await api.get('/letters/')
    letters.value = response.data
  } catch (error) {
    console.error('获取信件失败:', error)
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return dayjs(date).format('YYYY年MM月DD日')
}

const openLetter = (id) => {
  router.push(`/letters/${id}`)
}

onMounted(() => {
  fetchLetters()
})
</script>

<style scoped>
.letters-page {
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

.shape-3 {
  width: 250px;
  height: 250px;
  background: #3b82f6;
  top: 40%;
  right: 30%;
  animation-delay: 14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(30px, 20px) rotate(90deg); }
  50% { transform: translate(0, 40px) rotate(180deg); }
  75% { transform: translate(-30px, 20px) rotate(270deg); }
}

.page-header {
  position: relative;
  z-index: 10;
}

.header-left {
  display: flex;
  flex-direction: column;
}

.back-link {
  font-size: 0.95rem;
  font-weight: 500;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  backdrop-filter: blur(4px);
  width: fit-content;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #fef3c7, #fce7f3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(236, 72, 153, 0.25), inset 0 4px 0 rgba(255, 255, 255, 0.8);
  animation: logoFloat 4s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes logoFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-10px) rotate(2deg); }
  50% { transform: translateY(0) rotate(0deg); }
  75% { transform: translateY(-5px) rotate(-2deg); }
}

.logo-text {
  background: linear-gradient(135deg, #ec4899 0%, #f97316 50%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.logo-subtitle {
  font-weight: 500;
}

.write-btn {
  text-decoration: none;
}

.empty-state {
  position: relative;
  z-index: 10;
}

.empty-icon {
  animation: emptyFloat 3s ease-in-out infinite;
}

@keyframes emptyFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-15px) scale(1.05); }
}

.envelopes-grid {
  position: relative;
  z-index: 10;
}

.envelope-wrapper {
  perspective: 1500px;
  animation: fadeInUp 0.8s ease forwards;
  opacity: 0;
  transform: translateY(50px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.envelope-container {
  position: relative;
  cursor: pointer;
}

.envelope {
  position: relative;
  width: 100%;
  height: 190px;
  animation: envelopeFloat 4s ease-in-out infinite;
}

@keyframes envelopeFloat {
  0%, 100% { transform: translateY(0) rotateX(0deg); }
  50% { transform: translateY(-10px) rotateX(1deg); }
}

.envelope-shadow {
  position: absolute;
  bottom: -15px;
  left: 10%;
  right: 10%;
  height: 25px;
  background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.2), transparent);
  border-radius: 50%;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.envelope-container:hover .envelope-shadow {
  transform: scale(0.8);
  opacity: 0.5;
}

.envelope-back {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, #fde68a, #fbbf24);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15), inset 0 2px 0 rgba(255, 255, 255, 0.5);
}

.letter-paper {
  position: absolute;
  top: 22px;
  left: 50%;
  transform: translateX(-50%);
  width: 85%;
  height: 120px;
  background: linear-gradient(180deg, #ffffff 0%, #fef9c3 100%);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
  overflow: hidden;
}

.envelope-container:hover .letter-paper {
  transform: translateX(-50%) translateY(-40px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
}

.paper-content {
  padding: 10px 12px;
  height: 100%;
  background-image: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 20px,
    rgba(236, 72, 153, 0.05) 20px,
    rgba(236, 72, 153, 0.05) 21px
  );
}

.paper-title {
  margin-bottom: 4px;
  color: #1f2937;
  font-size: 0.85rem !important;
}

.paper-date {
  color: #9ca3af;
  font-size: 0.65rem;
}

.paper-preview {
  line-height: 1.4;
  color: #6b7280;
  font-size: 0.7rem;
}

.envelope-front {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
}

.envelope-flap {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 72px;
  background: linear-gradient(135deg, #f97316, #ea580c);
  border-radius: 16px 16px 0 0;
  z-index: 3;
  transform-origin: top;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  clip-path: polygon(0 0, 100% 0, 50% 100%);
}

.envelope-container:hover .envelope-flap {
  transform: rotateX(-160deg);
  transition-delay: 0.1s;
}

.flap-seal {
  position: absolute;
  top: 15px;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  height: 32px;
  background: radial-gradient(circle at 30% 30%, #fef3c7, #fbbf24);
  border-radius: 50%;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.25), inset 0 2px 0 rgba(255, 255, 255, 0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.envelope-container:hover .flap-seal {
  opacity: 0;
  transform: translateX(-50%) rotate(180deg);
}

.envelope-body {
  position: absolute;
  top: 36px;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, #fef9c3, #fde68a);
  border-radius: 0 0 16px 16px;
  padding: 12px;
  z-index: 2;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1), inset 0 2px 0 rgba(255, 255, 255, 0.5);
}

.stamp {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #ec4899, #be185d);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.2), inset 0 2px 0 rgba(255, 255, 255, 0.3);
  border: 3px dashed #fff;
  animation: stampFloat 3s ease-in-out infinite;
}

@keyframes stampFloat {
  0%, 100% { transform: translateY(0) rotate(-5deg); }
  50% { transform: translateY(-8px) rotate(5deg); }
}

.envelope-label {
  position: absolute;
  top: 16px;
  left: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.9);
  padding: 6px 12px;
  border-radius: 50px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.label-icon {
  font-size: 0.9rem;
}

.label-text {
  font-weight: 600;
  color: #374151;
  font-size: 0.75rem;
}

.unlock-date {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.9);
  padding: 5px 12px;
  border-radius: 10px;
  font-size: 0.72rem;
  color: #ec4899;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-weight: 500;
  white-space: nowrap;
}

.unlock-label {
  font-weight: 600;
  margin-right: 4px;
  color: #be185d;
}

.lock-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  animation: lockPulse 2s ease-in-out infinite;
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.2));
}

@keyframes lockPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.15); }
}

@media (max-width: 1200px) {
  .envelopes-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 900px) {
  .envelopes-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 640px) {
  .envelopes-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .logo-icon {
    width: 55px;
    height: 55px;
  }
  
  .logo-text {
    font-size: 1.5rem;
  }
  
  .envelope {
    height: 170px;
  }
  
  .letter-paper {
    height: 100px;
  }
}
</style>
