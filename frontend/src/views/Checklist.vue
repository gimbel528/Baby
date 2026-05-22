<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
    <div class="container mx-auto px-4 py-8">
      <div class="mb-6">
        <button
          @click="goBack"
          class="flex items-center text-gray-600 hover:text-gray-800 transition-colors mb-4"
        >
          <span class="mr-2">←</span>
          返回导航页
        </button>
        
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-4xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-2">
              {{ moduleInfo?.icon }} {{ moduleInfo?.name }}
            </h1>
            <p v-if="moduleInfo?.description" class="text-gray-600">{{ moduleInfo.description }}</p>
          </div>
          
          <button
            @click="showAddItem = true"
            class="px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-lg hover:from-pink-600 hover:to-purple-600 transition-all shadow-lg hover:shadow-xl"
          >
            ➕ 添加物品
          </button>
        </div>
      </div>

      <div class="mb-6">
        <div class="flex gap-2 flex-wrap">
          <button
            @click="selectedCategory = null"
            :class="[
              'px-4 py-2 rounded-lg transition-all',
              selectedCategory === null
                ? 'bg-purple-500 text-white'
                : 'bg-white text-gray-700 hover:bg-purple-50'
            ]"
          >
            全部
          </button>
          <button
            v-for="category in categories"
            :key="category.id"
            @click="selectedCategory = category.id"
            :class="[
              'px-4 py-2 rounded-lg transition-all',
              selectedCategory === category.id
                ? 'bg-purple-500 text-white'
                : 'bg-white text-gray-700 hover:bg-purple-50'
            ]"
          >
            {{ category.name }}
          </button>
          <button
            @click="showAddCategory = true"
            class="px-4 py-2 bg-white text-gray-500 rounded-lg hover:bg-gray-50 transition-all border-2 border-dashed border-gray-300"
          >
            ➕ 添加分类
          </button>
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div class="grid grid-cols-12 gap-4 px-6 py-4 bg-gray-50 font-semibold text-gray-700">
          <div class="col-span-1">状态</div>
          <div class="col-span-3">物品名称</div>
          <div class="col-span-2">分类</div>
          <div class="col-span-1">数量</div>
          <div class="col-span-2">链接</div>
          <div class="col-span-2">备注</div>
          <div class="col-span-1">操作</div>
        </div>

        <div v-if="filteredItems.length === 0" class="px-6 py-12 text-center text-gray-500">
          <div class="text-6xl mb-4">📦</div>
          <p>还没有添加任何物品</p>
          <p class="text-sm mt-2">点击右上角的"添加物品"开始吧！</p>
        </div>

        <div
          v-for="item in filteredItems"
          :key="item.id"
          class="grid grid-cols-12 gap-4 px-6 py-4 border-b border-gray-100 hover:bg-gray-50 transition-colors items-center"
        >
          <div class="col-span-1">
            <select
              v-model="item.status"
              @change="updateItemStatus(item)"
              :class="[
                'w-full px-2 py-1 rounded-lg text-sm font-medium border-2 cursor-pointer',
                statusStyles[item.status]
              ]"
            >
              <option value="pending">待购买</option>
              <option value="purchased">已购买</option>
              <option value="packed">已打包</option>
              <option value="ready">已准备</option>
            </select>
          </div>
          
          <div class="col-span-3 font-medium text-gray-800">
            {{ item.name }}
          </div>
          
          <div class="col-span-2 text-gray-600">
            {{ getCategoryName(item.category_id) }}
          </div>
          
          <div class="col-span-1 text-gray-600">
            {{ item.quantity }}
          </div>
          
          <div class="col-span-2">
            <a
              v-if="item.link"
              :href="item.link"
              target="_blank"
              class="text-blue-500 hover:text-blue-600 text-sm"
            >
              🔗 查看链接
            </a>
            <span v-else class="text-gray-400 text-sm">-</span>
          </div>
          
          <div class="col-span-2 text-gray-600 text-sm">
            {{ item.notes || '-' }}
          </div>
          
          <div class="col-span-1 flex gap-2">
            <button
              @click="editItem(item)"
              class="text-blue-500 hover:text-blue-600 transition-colors"
            >
              ✏️
            </button>
            <button
              @click="deleteItem(item.id)"
              class="text-red-500 hover:text-red-600 transition-colors"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="showAddCategory"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        @click="showAddCategory = false"
      >
        <div
          class="bg-white rounded-2xl p-8 w-full max-w-md shadow-2xl"
          @click.stop
        >
          <h2 class="text-2xl font-bold text-gray-800 mb-6">添加分类</h2>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">分类名称</label>
            <input
              v-model="newCategory.name"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="例如：妈妈用品、宝宝用品"
            />
          </div>

          <div class="flex gap-4 mt-6">
            <button
              @click="showAddCategory = false"
              class="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              @click="createCategory"
              :disabled="!newCategory.name"
              class="flex-1 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-lg hover:from-pink-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              创建
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="showAddItem"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        @click="showAddItem = false"
      >
        <div
          class="bg-white rounded-2xl p-8 w-full max-w-lg shadow-2xl"
          @click.stop
        >
          <h2 class="text-2xl font-bold text-gray-800 mb-6">
            {{ editingItem ? '编辑物品' : '添加物品' }}
          </h2>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">物品名称 *</label>
              <input
                v-model="itemForm.name"
                type="text"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="例如：奶瓶、尿不湿"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">分类</label>
              <select
                v-model="itemForm.category_id"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option :value="null">无分类</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">数量</label>
                <input
                  v-model.number="itemForm.quantity"
                  type="number"
                  min="1"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">状态</label>
                <select
                  v-model="itemForm.status"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="pending">待购买</option>
                  <option value="purchased">已购买</option>
                  <option value="packed">已打包</option>
                  <option value="ready">已准备</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">购买链接</label>
              <input
                v-model="itemForm.link"
                type="url"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="https://..."
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">备注</label>
              <textarea
                v-model="itemForm.notes"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                rows="3"
                placeholder="其他需要记录的信息"
              ></textarea>
            </div>
          </div>

          <div class="flex gap-4 mt-6">
            <button
              @click="cancelItemEdit"
              class="flex-1 px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              @click="saveItem"
              :disabled="!itemForm.name"
              class="flex-1 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-lg hover:from-pink-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ editingItem ? '保存' : '添加' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const moduleId = route.params.id

const moduleInfo = ref(null)
const categories = ref([])
const items = ref([])
const selectedCategory = ref(null)
const showAddCategory = ref(false)
const showAddItem = ref(false)
const editingItem = ref(null)

const newCategory = ref({
  name: ''
})

const itemForm = ref({
  name: '',
  category_id: null,
  quantity: 1,
  status: 'pending',
  link: '',
  notes: ''
})

const statusStyles = {
  pending: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  purchased: 'bg-blue-100 text-blue-800 border-blue-300',
  packed: 'bg-purple-100 text-purple-800 border-purple-300',
  ready: 'bg-green-100 text-green-800 border-green-300'
}

const filteredItems = computed(() => {
  if (!selectedCategory.value) {
    return items.value
  }
  return items.value.filter(item => item.category_id === selectedCategory.value)
})

const fetchModuleInfo = async () => {
  try {
    const response = await api.get('/checklist/modules')
    moduleInfo.value = response.data.find(m => m.id === moduleId)
  } catch (error) {
    console.error('获取模块信息失败:', error)
  }
}

const fetchCategories = async () => {
  try {
    const response = await api.get('/checklist/categories', {
      params: { module_id: moduleId }
    })
    categories.value = response.data
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

const fetchItems = async () => {
  try {
    const response = await api.get('/checklist/items', {
      params: { module_id: moduleId }
    })
    items.value = response.data
  } catch (error) {
    console.error('获取物品失败:', error)
  }
}

const getCategoryName = (categoryId) => {
  if (!categoryId) return '-'
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || '-'
}

const createCategory = async () => {
  if (!newCategory.value.name) {
    alert('请输入分类名称')
    return
  }

  try {
    await api.post('/checklist/categories', {
      ...newCategory.value,
      module_id: moduleId
    })
    showAddCategory.value = false
    newCategory.value = { name: '' }
    await fetchCategories()
  } catch (error) {
    console.error('创建分类失败:', error)
    alert('创建失败，请重试')
  }
}

const editItem = (item) => {
  editingItem.value = item
  itemForm.value = {
    name: item.name,
    category_id: item.category_id,
    quantity: item.quantity,
    status: item.status,
    link: item.link,
    notes: item.notes
  }
  showAddItem.value = true
}

const cancelItemEdit = () => {
  showAddItem.value = false
  editingItem.value = null
  itemForm.value = {
    name: '',
    category_id: null,
    quantity: 1,
    status: 'pending',
    link: '',
    notes: ''
  }
}

const saveItem = async () => {
  if (!itemForm.value.name) {
    alert('请输入物品名称')
    return
  }

  try {
    const data = {
      ...itemForm.value,
      module_id: moduleId
    }

    if (editingItem.value) {
      await api.patch(`/checklist/items/${editingItem.value.id}`, data)
    } else {
      await api.post('/checklist/items', data)
    }

    cancelItemEdit()
    await fetchItems()
  } catch (error) {
    console.error('保存物品失败:', error)
    alert('保存失败，请重试')
  }
}

const updateItemStatus = async (item) => {
  try {
    await api.patch(`/checklist/items/${item.id}`, {
      status: item.status
    })
  } catch (error) {
    console.error('更新状态失败:', error)
    alert('更新失败，请重试')
    await fetchItems()
  }
}

const deleteItem = async (itemId) => {
  if (!confirm('确定要删除这个物品吗？')) {
    return
  }

  try {
    await api.delete(`/checklist/items/${itemId}`)
    await fetchItems()
  } catch (error) {
    console.error('删除物品失败:', error)
    alert('删除失败，请重试')
  }
}

const goBack = () => {
  router.push('/dashboard')
}

onMounted(() => {
  fetchModuleInfo()
  fetchCategories()
  fetchItems()
})
</script>

<style scoped>
</style>
