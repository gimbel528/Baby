<template>
  <div class="card min-h-[420px] flex flex-col justify-center items-center relative overflow-hidden rounded-[32px]">
    <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-pink-100/40 via-purple-50/30 to-blue-100/40"></div>
    
    <div class="absolute top-8 left-8 text-6xl opacity-30 animate-float" style="animation-delay: 0s">🌸</div>
    <div class="absolute bottom-12 right-12 text-5xl opacity-30 animate-float" style="animation-delay: 1.5s">⭐</div>
    <div class="absolute top-20 right-20 text-4xl opacity-20 animate-float" style="animation-delay: 0.8s">🌙</div>
    
    <div class="relative z-10 text-center px-6">
      <div v-if="activeEvent">
        <div class="inline-flex items-center gap-2 px-4 py-2 bg-white/70 backdrop-blur-sm rounded-full mb-8 shadow-sm">
          <span class="text-xl">🎯</span>
          <h2 class="text-lg md:text-xl font-semibold text-gray-700">
            距离 {{ activeEvent.event_name }}
          </h2>
        </div>
        
        <div class="flex justify-center items-center gap-4 md:gap-6 mb-8">
          <div class="text-center">
            <div class="text-7xl md:text-8xl font-display font-bold text-gradient mb-2">
              {{ Math.abs(activeEvent.days_remaining) }}
            </div>
            <div class="text-lg md:text-xl text-gray-600 font-medium">天</div>
          </div>
        </div>

        <div class="inline-flex items-center gap-2 px-6 py-3 bg-white/80 backdrop-blur-sm rounded-full shadow-sm">
          <div v-if="activeEvent.is_expired" class="text-gray-600">
            <span class="text-2xl mr-2">🎉</span>
            已经过去啦！
          </div>
          <div v-else class="text-gray-600">
            <span class="text-2xl mr-2">🌟</span>
            期待中...
          </div>
        </div>
      </div>

      <div v-else class="text-gray-500">
        <div class="text-8xl mb-6 animate-bounce">📅</div>
        <p class="text-xl font-medium text-gray-700 mb-2">还没有倒计时事件</p>
        <p class="text-base text-gray-500">添加一个倒计时开始记录吧！</p>
      </div>
    </div>

    <div v-if="events.length > 1" class="absolute bottom-6 left-0 right-0 flex justify-center gap-3">
      <button 
        v-for="(event, index) in events" 
        :key="event.id"
        @click="currentIndex = index"
        class="h-3 rounded-full transition-all duration-300"
        :class="currentIndex === index ? 'w-10 bg-gradient-to-r from-pink-400 to-purple-500' : 'w-3 bg-gray-300 hover:bg-gray-400'"
      ></button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  events: {
    type: Array,
    default: () => []
  }
})

const currentIndex = ref(0)

const activeEvent = computed(() => {
  return props.events[currentIndex.value] || null
})
</script>

<style scoped>
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(3deg); }
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.animate-bounce {
  animation: bounce 2s ease-in-out infinite;
}
</style>
