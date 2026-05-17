<template>
  <div class="card min-h-[300px] flex flex-col justify-center items-center relative overflow-hidden">
    <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-baby-pink/20 via-transparent to-baby-blue/20"></div>
    
    <div class="relative z-10 text-center">
      <div v-if="activeEvent" class="animate-float">
        <h2 class="text-xl md:text-2xl font-semibold text-gray-700 mb-6">
          距离 {{ activeEvent.event_name }}
        </h2>
        
        <div class="flex justify-center items-center gap-4 md:gap-6 mb-6">
          <div class="text-center">
            <div class="text-5xl md:text-7xl font-display font-bold text-gradient">
              {{ Math.abs(activeEvent.days_remaining) }}
            </div>
            <div class="text-sm md:text-base text-gray-600 mt-2">天</div>
          </div>
        </div>

        <div v-if="activeEvent.is_expired" class="text-lg text-gray-600">
          🎉 已经过去啦！
        </div>
        <div v-else class="text-lg text-gray-600">
          🌟 期待中...
        </div>
      </div>

      <div v-else class="text-gray-500">
        <div class="text-6xl mb-4">📅</div>
        <p class="text-lg">还没有倒计时事件</p>
        <p class="text-sm mt-2">添加一个倒计时开始记录吧！</p>
      </div>
    </div>

    <div v-if="events.length > 1" class="absolute bottom-4 left-0 right-0 flex justify-center gap-2">
      <button 
        v-for="(event, index) in events" 
        :key="event.id"
        @click="currentIndex = index"
        class="w-2 h-2 rounded-full transition-all duration-300"
        :class="currentIndex === index ? 'bg-primary-500 w-6' : 'bg-gray-300'"
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
