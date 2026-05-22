<template>
  <div class="min-h-screen health-page">
    <div class="floating-bg">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
    </div>

    <div class="max-w-4xl mx-auto px-4 py-8 relative z-10">
      <header class="page-header mb-8">
        <router-link to="/dashboard" class="back-link inline-flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-all hover:translate-x-1 mb-4">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
          </svg>
          返回
        </router-link>

        <div class="header-content flex flex-col md:flex-row justify-between items-center gap-4">
          <div>
            <h1 class="text-2xl md:text-3xl font-bold text-gradient flex items-center gap-3">
              <span class="text-3xl">📋</span>
              健康档案
            </h1>
            <p class="text-gray-600 mt-2">记录宝宝成长的每一步</p>
          </div>
          <button
            @click="showAddModal = true"
            class="add-btn flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-pink-500 to-purple-500 text-white font-semibold shadow-lg hover:shadow-xl transition-all hover:scale-105"
          >
            <span class="text-xl">+</span>
            添加记录
          </button>
        </div>
      </header>

      <div v-if="isLoading" class="loading-state text-center py-20">
        <div class="empty-icon text-6xl mb-6 animate-bounce">⏳</div>
        <p class="text-xl text-gray-600">加载中...</p>
      </div>

      <div v-else-if="records.length === 0" class="empty-state text-center py-20">
        <div class="empty-icon text-6xl mb-6 animate-bounce">📋</div>
        <h2 class="text-2xl font-semibold mb-4 text-gray-800">还没有健康记录</h2>
        <p class="text-gray-600 mb-8">点击上方按钮添加第一条记录</p>
      </div>

      <div v-else class="records-list space-y-4">
        <div
          v-for="record in records"
          :key="record.id"
          class="record-card bg-white/90 backdrop-blur-lg rounded-2xl p-6 shadow-md hover:shadow-lg transition-all"
        >
          <div class="flex flex-col md:flex-row gap-4">
            <div class="flex-1">
              <div class="flex items-start gap-4">
                <div class="type-icon flex-shrink-0 w-12 h-12 rounded-xl flex items-center justify-center text-2xl" :class="getTypeBgClass(record.record_type)">
                  {{ getTypeIcon(record.record_type) }}
                </div>
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-gray-800">{{ record.title }}</h3>
                  <p v-if="record.value" class="text-purple-600 font-semibold mt-1">{{ record.value }}</p>
                  <p v-if="record.notes" class="text-gray-600 mt-2">{{ record.notes }}</p>
                </div>
              </div>
            </div>

            <div class="flex flex-col md:flex-row items-start md:items-center gap-4">
              <div class="date-badge flex-shrink-0 text-sm text-gray-600">
                {{ record.date ? formatDate(record.date) : '—' }}
              </div>

              <div class="flex gap-2 flex-shrink-0">
                <button
                  @click="editRecord(record)"
                  class="action-btn w-9 h-9 flex items-center justify-center rounded-xl text-gray-500 hover:bg-gray-100 transition-all"
                >
                  ✏️
                </button>
                <button
                  @click="deleteRecord(record.id)"
                  class="action-btn w-9 h-9 flex items-center justify-center rounded-xl text-gray-500 hover:bg-red-50 hover:text-red-600 transition-all"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showAddModal || showEditModal"
        class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50"
        @click="closeModal"
      >
        <div
          class="modal-content bg-white rounded-3xl p-8 w-full max-w-lg shadow-2xl"
          @click.stop
        >
          <h2 class="text-2xl font-bold text-gray-800 mb-6">{{ showEditModal ? '编辑记录' : '添加健康记录' }}</h2>

          <div class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">记录类型 *</label>
              <select
                v-model="form.record_type"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
              >
                <option value="height">身高</option>
                <option value="weight">体重</option>
                <option value="sick">生病</option>
                <option value="injury">受伤</option>
                <option value="allergy">过敏</option>
                <option value="other">其他</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">标题 *</label>
              <input
                v-model="form.title"
                type="text"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                placeholder="例如：3个月体检"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">数值（可选）</label>
              <input
                v-model="form.value"
                type="text"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                placeholder="例如：60cm、5.5kg"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">日期</label>
              <input
                v-model="form.date"
                type="date"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">备注</label>
              <textarea
                v-model="form.notes"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                rows="3"
                placeholder="添加备注..."
              ></textarea>
            </div>
          </div>

          <div class="flex gap-4 mt-8">
            <button
              @click="closeModal"
              class="flex-1 px-6 py-3 border border-gray-200 rounded-xl text-gray-700 hover:bg-gray-50 transition-all"
            >
              取消
            </button>
            <button
              @click="saveRecord"
              :disabled="!form.title"
              class="flex-1 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-xl hover:from-pink-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
            >
              保存
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const route = useRoute()

const moduleId = route.params.id
const records = ref([])
const isLoading = ref(true)
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingId = ref(null)

const form = ref({
  record_type: 'other',
  title: '',
  value: '',
  date: '',
  notes: '',
  module_id: moduleId
})

const fetchRecords = async () => {
  try {
    isLoading.value = true
    const response = await api.get(`/health/health/${moduleId}`)
    records.value = response.data
  } catch (error) {
    console.error('获取健康记录失败:', error)
  } finally {
    isLoading.value = false
  }
}

const editRecord = (record) => {
  editingId.value = record.id
  form.value = {
    record_type: record.record_type || 'other',
    title: record.title,
    value: record.value || '',
    date: record.date || '',
    notes: record.notes || '',
    module_id: moduleId
  }
  showEditModal.value = true
}

const saveRecord = async () => {
  if (!form.value.title) {
    alert('请填写标题')
    return
  }

  try {
    if (showEditModal.value && editingId.value) {
      await api.put(`/health/health/${editingId.value}`, form.value)
    } else {
      await api.post('/health/health', form.value)
    }
    closeModal()
    await fetchRecords()
  } catch (error) {
    console.error('保存记录失败:', error)
    alert('保存失败，请重试')
  }
}

const deleteRecord = async (recordId) => {
  if (!confirm('确定要删除这条记录吗？')) {
    return
  }

  try {
    await api.delete(`/health/health/${recordId}`)
    await fetchRecords()
  } catch (error) {
    console.error('删除记录失败:', error)
    alert('删除失败，请重试')
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  editingId.value = null
  form.value = {
    record_type: 'other',
    title: '',
    value: '',
    date: '',
    notes: '',
    module_id: moduleId
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

const getTypeIcon = (type) => {
  const icons = {
    height: '📏',
    weight: '⚖️',
    sick: '🤒',
    injury: '🩹',
    allergy: '⚠️',
    other: '📝'
  }
  return icons[type] || icons.other
}

const getTypeBgClass = (type) => {
  const classes = {
    height: 'bg-blue-100',
    weight: 'bg-green-100',
    sick: 'bg-red-100',
    injury: 'bg-orange-100',
    allergy: 'bg-yellow-100',
    other: 'bg-gray-100'
  }
  return classes[type] || classes.other
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.health-page {
  background: linear-gradient(135deg, #dbeafe 0%, #fce7f3 100%);
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
  background: #3b82f6;
  top: -150px;
  right: -150px;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #ec4899;
  bottom: -100px;
  left: -100px;
  animation-delay: 7s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, -20px); }
}

.page-header {
  position: relative;
  z-index: 10;
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

.text-gradient {
  background: linear-gradient(135deg, #3b82f6 0%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.add-btn {
  border: none;
  cursor: pointer;
}

.loading-state, .empty-state {
  position: relative;
  z-index: 10;
}

.empty-icon {
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.records-list {
  position: relative;
  z-index: 10;
}

.record-card {
  transition: all 0.3s ease;
}

.record-card:hover {
  transform: translateY(-2px);
}

.type-icon {
  transition: transform 0.3s ease;
}

.record-card:hover .type-icon {
  transform: scale(1.1);
}

.date-badge {
  background: rgba(148, 163, 184, 0.1);
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 500;
}

.action-btn {
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.input-field {
  outline: none;
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

@media (max-width: 640px) {
  .record-card {
    padding: 20px;
  }
}
</style>
