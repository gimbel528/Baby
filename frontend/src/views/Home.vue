<template>
  <div class="min-h-screen p-4 md:p-8 home-page">
    <div class="floating-bg">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
    </div>
    
    <div class="max-w-6xl mx-auto relative z-10">
      <header class="flex justify-between items-center mb-12">
        <div class="logo-wrapper">
          <h1 class="text-3xl md:text-4xl font-display font-bold text-gradient">
            宝宝成长记录
          </h1>
          <div class="logo-dots flex gap-1 mt-2">
            <span class="w-2 h-2 rounded-full bg-pink-400 animate-pulse"></span>
            <span class="w-2 h-2 rounded-full bg-yellow-400 animate-pulse" style="animation-delay: 0.2s"></span>
            <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse" style="animation-delay: 0.4s"></span>
          </div>
        </div>
        <button 
          @click="handleLogout"
          class="logout-btn flex items-center gap-2 px-4 py-2 rounded-xl hover:bg-white/80 transition-all hover:scale-105"
        >
          <span>👋</span>
          <span>退出登录</span>
        </button>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
        <div class="lg:col-span-2">
          <div class="countdown-wrapper">
            <CountdownTimer :events="countdownEvents" @refresh="fetchCountdownEvents" />
          </div>
        </div>
        
        <div class="quick-actions">
          <h2 class="text-xl font-semibold mb-6 text-gray-800">
            <span class="inline-block mr-2">⚡</span>
            快速操作
          </h2>
          <div class="space-y-4">
            <router-link to="/write" class="quick-action primary flex items-center justify-center gap-3">
              <span class="text-2xl">✉️</span>
              <span>写一封信</span>
            </router-link>
            <router-link to="/letters" class="quick-action secondary flex items-center justify-center gap-3">
              <span class="text-2xl">📚</span>
              <span>查看信件</span>
            </router-link>
          </div>
          
          <div class="stats-card mt-8">
            <div class="stat-item">
              <div class="stat-number text-gradient text-3xl font-bold">{{ lettersCount }}</div>
              <div class="stat-label text-gray-600">已写信件</div>
            </div>
            <div class="stat-divider w-px h-12 bg-gradient-to-b from-transparent via-gray-300 to-transparent"></div>
            <div class="stat-item">
              <div class="stat-number text-gradient text-3xl font-bold">{{ eventsCount }}</div>
              <div class="stat-label text-gray-600">倒计时</div>
            </div>
          </div>
        </div>
      </div>

      <div class="events-card">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-2xl font-semibold flex items-center gap-3">
            <span class="inline-block w-2 h-8 bg-gradient-to-b from-pink-400 to-yellow-400 rounded-full"></span>
            倒计时事件
          </h2>
          <button 
            @click="showAddEvent = true"
            class="add-event-btn flex items-center gap-2 px-5 py-3 rounded-xl transition-all hover:scale-105"
          >
            <span class="text-xl">+</span>
            <span>添加事件</span>
          </button>
        </div>

        <div v-if="countdownEvents.length === 0" class="empty-state text-center py-16">
          <div class="empty-icon text-6xl mb-6 animate-bounce">⏰</div>
          <p class="text-xl text-gray-600 mb-2">还没有倒计时事件</p>
          <p class="text-gray-500">点击上方按钮添加第一个倒计时</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div 
            v-for="(event, index) in countdownEvents" 
            :key="event.id"
            class="event-card"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="event-header flex justify-between items-start mb-4">
              <h3 class="font-semibold text-xl">{{ event.event_name }}</h3>
              <div 
                class="days-badge"
                :class="event.is_expired ? 'expired' : 'active'"
              >
                {{ event.is_expired ? '已过期' : `${event.days_remaining} 天` }}
              </div>
            </div>
            <div class="event-date flex items-center gap-2 text-gray-600">
              <span class="text-lg">📅</span>
              <span>目标日期: {{ formatDate(event.target_date) }}</span>
            </div>
            <div class="event-progress mt-4">
              <div class="progress-bar bg-gray-200 rounded-full h-2 overflow-hidden">
                <div 
                  class="progress-fill h-full rounded-full bg-gradient-to-r from-pink-400 to-yellow-400"
                  :style="{ width: getProgressWidth(event) }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <AddEventModal 
      v-if="showAddEvent"
      @close="showAddEvent = false"
      @added="handleEventAdded"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import dayjs from 'dayjs'
import CountdownTimer from '@/components/CountdownTimer.vue'
import AddEventModal from '@/components/AddEventModal.vue'

const router = useRouter()
const authStore = useAuthStore()

const countdownEvents = ref([])
const lettersCount = ref(0)
const showAddEvent = ref(false)

const eventsCount = computed(() => countdownEvents.value.length)

const fetchCountdownEvents = async () => {
  try {
    const response = await api.get('/countdown/')
    countdownEvents.value = response.data
  } catch (error) {
    console.error('获取倒计时事件失败:', error)
  }
}

const fetchLettersCount = async () => {
  try {
    const response = await api.get('/letters/')
    lettersCount.value = response.data.length
  } catch (error) {
    console.error('获取信件数量失败:', error)
  }
}

const formatDate = (date) => {
  return dayjs(date).format('YYYY年MM月DD日')
}

const getProgressWidth = (event) => {
  if (event.is_expired) return '100%'
  const totalDays = 365
  const progress = Math.min(((totalDays - event.days_remaining) / totalDays) * 100, 100)
  return `${progress}%`
}

const handleEventAdded = async () => {
  showAddEvent.value = false
  await fetchCountdownEvents()
  console.log('刷新事件成功，当前事件数:', countdownEvents.value.length)
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchCountdownEvents()
  fetchLettersCount()
})
</script>

<style scoped>
.home-page {
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
  opacity: 0.1;
  animation: float 20s ease-in-out infinite;
}

.shape-1 {
  width: 300px;
  height: 300px;
  background: #ec4899;
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 400px;
  height: 400px;
  background: #f97316;
  bottom: -150px;
  left: -150px;
  animation-delay: 5s;
}

.shape-3 {
  width: 200px;
  height: 200px;
  background: #3b82f6;
  top: 50%;
  left: 50%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(50px, 50px) rotate(90deg); }
  50% { transform: translate(0, 100px) rotate(180deg); }
  75% { transform: translate(-50px, 50px) rotate(270deg); }
}

.logout-btn {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #4b5563;
}

.countdown-wrapper {
  position: relative;
}

.quick-actions {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.5);
}

.quick-action {
  padding: 16px 24px;
  border-radius: 16px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.quick-action.primary {
  background: linear-gradient(135deg, #ec4899, #f97316);
  color: white;
  box-shadow: 0 4px 20px rgba(236, 72, 153, 0.3);
}

.quick-action.primary:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 30px rgba(236, 72, 153, 0.4);
}

.quick-action.secondary {
  background: white;
  color: #4b5563;
  border: 2px solid #e5e7eb;
}

.quick-action.secondary:hover {
  border-color: #ec4899;
  color: #ec4899;
  transform: translateY(-2px);
}

.stats-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 6px;
  padding-top: 24px;
  border-top: 1px dashed #e5e7eb;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.events-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 36px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.5);
}

.add-event-btn {
  background: linear-gradient(135deg, #ec4899, #f97316);
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 20px rgba(236, 72, 153, 0.3);
}

.add-event-btn:hover {
  box-shadow: 0 6px 25px rgba(236, 72, 153, 0.4);
}

.empty-icon {
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.event-card {
  background: linear-gradient(145deg, #ffffff, #fef3c7);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeInUp 0.6s ease both;
  border: 1px solid rgba(255, 255, 255, 0.8);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.event-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}

.days-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
}

.days-badge.active {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(249, 115, 22, 0.1));
  color: #ec4899;
}

.days-badge.expired {
  background: #f3f4f6;
  color: #9ca3af;
}

.progress-fill {
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .events-card {
    padding: 24px;
  }
  
  .quick-actions {
    padding: 24px;
  }
  
  .floating-shape {
    display: none;
  }
}
</style>
