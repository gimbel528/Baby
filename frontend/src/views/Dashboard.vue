<template>
  <div class="min-h-screen dashboard-page">
    <div class="floating-bg">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
    </div>

    <div class="max-w-6xl mx-auto px-4 py-8 relative z-10">
      <header class="page-header flex flex-col md:flex-row justify-between items-center mb-10">
        <div class="header-left text-center md:text-left mb-6 md:mb-0">
          <router-link to="/" class="back-link inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-all hover:translate-x-1 mb-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            返回首页
          </router-link>
          
          <div class="logo-container">
            <div class="logo-icon">
              <span class="text-4xl">💝</span>
            </div>
            <h1 class="logo-text text-2xl md:text-3xl font-bold text-gradient">
              爱的记录
            </h1>
            <p class="logo-subtitle text-gray-600 mt-2 text-sm">
              物品·疫苗·健康，给宝宝完整的爱
            </p>
          </div>
        </div>
      </header>

      <div v-if="coreModules.length === 0" class="empty-state text-center py-20">
        <div class="empty-icon text-6xl mb-6 animate-bounce">⏳</div>
        <h2 class="text-2xl font-semibold mb-4 text-gray-800">加载中</h2>
        <p class="text-gray-600 mb-8 text-base">请稍候，正在准备模块</p>
      </div>

      <div v-else class="modules-grid grid grid-cols-1 md:grid-cols-3 gap-6">
        <div 
          v-for="(module, index) in coreModules" 
          :key="module.id"
          class="module-wrapper"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="module-card group cursor-pointer" @click="goToModule(module)">
            <div class="module-card-inner">
              <div class="module-icon-wrapper mb-4">
                <span class="module-icon text-5xl">{{ module.icon }}</span>
                <div class="module-icon-bg"></div>
              </div>
              
              <h3 class="module-name text-xl font-bold text-gray-800 mb-2">{{ module.name }}</h3>
              <p v-if="module.description" class="module-desc text-gray-500 text-sm mb-4 line-clamp-2">{{ module.description }}</p>
              
              <div class="module-footer flex items-center justify-between pt-4 border-t border-gray-100">
                <div class="module-arrow text-gray-400 group-hover:text-purple-500 transition-colors">
                  <svg class="w-6 h-6 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </div>
              </div>
            </div>
            
            <div class="module-glow"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const modules = ref([])

const coreModules = computed(() => {
  const coreNames = ['物品明细', '疫苗记录', '健康档案']
  return modules.value.filter(m => coreNames.includes(m.name))
})

const fetchModules = async () => {
  try {
    const response = await api.get('/checklist/modules')
    modules.value = response.data
  } catch (error) {
    console.error('获取功能模块失败:', error)
  }
}

const goToModule = (module) => {
  const moduleType = module.module_type || 'custom'
  
  if (moduleType === 'vaccine') {
    router.push(`/vaccine/${module.id}`)
  } else if (moduleType === 'health') {
    router.push(`/health/${module.id}`)
  } else {
    router.push(`/checklist/${module.id}`)
  }
}

onMounted(() => {
  fetchModules()
})
</script>

<style scoped>
.dashboard-page {
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
  background: #a855f7;
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
  text-decoration: none;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #fce7f3, #ede9fe);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.25), inset 0 4px 0 rgba(255, 255, 255, 0.8);
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
  background: linear-gradient(135deg, #ec4899 0%, #a855f7 50%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.logo-subtitle {
  font-weight: 500;
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

.add-btn {
  border: none;
  cursor: pointer;
}

.modules-grid {
  position: relative;
  z-index: 10;
}

.module-wrapper {
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  transform: translateY(30px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.module-card {
  position: relative;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.module-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(139, 92, 246, 0.15);
}

.module-card-inner {
  position: relative;
  padding: 28px;
  z-index: 1;
}

.module-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at top left, rgba(168, 85, 247, 0.1), transparent 50%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.module-card:hover .module-glow {
  opacity: 1;
}

.delete-btn {
  z-index: 10;
}

.module-icon-wrapper {
  position: relative;
  display: inline-block;
}

.module-icon-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(168, 85, 247, 0.1));
  border-radius: 50%;
  z-index: 0;
}

.module-icon {
  position: relative;
  z-index: 1;
  display: inline-block;
  animation: iconBounce 3s ease-in-out infinite;
}

@keyframes iconBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.module-desc {
  line-height: 1.5;
}

.module-footer {
  margin-top: auto;
}

.module-card.add-card {
  background: rgba(255, 255, 255, 0.5);
  border: 2px dashed rgba(168, 85, 247, 0.3);
}

.module-card.add-card:hover {
  border-color: rgba(168, 85, 247, 0.6);
  background: rgba(255, 255, 255, 0.7);
}

.add-icon-wrapper {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(139, 92, 246, 0.1));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.module-card.add-card:hover .add-icon-wrapper {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(139, 92, 246, 0.2));
  transform: scale(1.05);
}

.add-icon {
  color: #9ca3af;
  transition: color 0.3s ease;
}

.module-card.add-card:hover .add-icon {
  color: #8b5cf6;
}

.modal-content {
  animation: modalIn 0.3s ease;
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.input-field {
  outline: none;
}

.icon-btn {
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  transform: scale(1.1);
}

@media (max-width: 1024px) {
  .modules-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .modules-grid {
    grid-template-columns: 1fr;
  }
  
  .logo-icon {
    width: 55px;
    height: 55px;
  }
  
  .logo-text {
    font-size: 1.5rem;
  }
  
  .module-card-inner {
    padding: 24px;
  }
}
</style>
