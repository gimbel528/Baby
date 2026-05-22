<template>
  <div class="min-h-screen vaccine-page">
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
              <span class="text-3xl">💉</span>
              疫苗记录
            </h1>
            <p class="text-gray-600 mt-2">记录宝宝每一次疫苗接种</p>
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
        <div class="empty-icon text-6xl mb-6 animate-bounce">💉</div>
        <h2 class="text-2xl font-semibold mb-4 text-gray-800">还没有疫苗记录</h2>
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
                <div class="age-badge flex-shrink-0 bg-gradient-to-r from-pink-100 to-purple-100 text-purple-700 px-4 py-2 rounded-xl font-semibold">
                  {{ record.age || '—' }}
                </div>
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-gray-800">{{ record.name }}</h3>
                  <p v-if="record.notes" class="text-gray-600 mt-2">{{ record.notes }}</p>
                </div>
              </div>
            </div>

            <div class="flex flex-col md:flex-row items-start md:items-center gap-4">
              <div class="dates flex flex-col text-sm text-gray-600">
                <div class="flex items-center gap-2">
                  <span class="text-gray-400">计划：</span>
                  <span>{{ record.scheduled_date ? formatDate(record.scheduled_date) : '—' }}</span>
                </div>
                <div class="flex items-center gap-2 mt-1">
                  <span class="text-gray-400">实际：</span>
                  <span>{{ record.actual_date ? formatDate(record.actual_date) : '—' }}</span>
                </div>
              </div>

              <div class="status-badge flex-shrink-0" :class="getStatusClass(record.status)">
                {{ getStatusText(record.status) }}
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
          <h2 class="text-2xl font-bold text-gray-800 mb-6">{{ showEditModal ? '编辑记录' : '添加疫苗记录' }}</h2>

          <div class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">疫苗名称 *</label>
              <input
                v-model="form.name"
                type="text"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                placeholder="例如：卡介苗"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">月龄/年龄</label>
              <input
                v-model="form.age"
                type="text"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                placeholder="例如：出生、1月龄"
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">计划日期</label>
                <input
                  v-model="form.scheduled_date"
                  type="date"
                  class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">实际日期</label>
                <input
                  v-model="form.actual_date"
                  type="date"
                  class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
              <select
                v-model="form.status"
                class="input-field w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
              >
                <option value="pending">待接种</option>
                <option value="done">已接种</option>
                <option value="missed">错过</option>
              </select>
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
              :disabled="!form.name"
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
  name: '',
  age: '',
  scheduled_date: '',
  actual_date: '',
  status: 'pending',
  notes: '',
  module_id: moduleId
})

const fetchRecords = async () => {
  try {
    isLoading.value = true
    const response = await api.get(`/health/vaccines/${moduleId}`)
    records.value = response.data
  } catch (error) {
    console.error('获取疫苗记录失败:', error)
  } finally {
    isLoading.value = false
  }
}

const editRecord = (record) => {
  editingId.value = record.id
  form.value = {
    name: record.name,
    age: record.age || '',
    scheduled_date: record.scheduled_date || '',
    actual_date: record.actual_date || '',
    status: record.status || 'pending',
    notes: record.notes || '',
    module_id: moduleId
  }
  showEditModal.value = true
}

const saveRecord = async () => {
  if (!form.value.name) {
    alert('请填写疫苗名称')
    return
  }

  try {
    if (showEditModal.value && editingId.value) {
      await api.put(`/health/vaccines/${editingId.value}`, form.value)
    } else {
      await api.post('/health/vaccines', form.value)
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
    await api.delete(`/health/vaccines/${recordId}`)
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
    name: '',
    age: '',
    scheduled_date: '',
    actual_date: '',
    status: 'pending',
    notes: '',
    module_id: moduleId
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    done: 'bg-green-100 text-green-700',
    missed: 'bg-red-100 text-red-700'
  }
  return classes[status] || classes.pending
}

const getStatusText = (status) => {
  const texts = {
    pending: '待接种',
    done: '已接种',
    missed: '错过'
  }
  return texts[status] || '待接种'
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.vaccine-page {
  background: linear-gradient(135deg, #fef3c7 0%, #fce7f3 100%);
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
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: #a855f7;
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
  background: linear-gradient(135deg, #ec4899 0%, #a855f7 100%);
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

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;
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
