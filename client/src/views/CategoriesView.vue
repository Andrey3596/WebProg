<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'


const categories = ref([])

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}


const categoryToAdd = ref({ name: '' })
const categoryAddPictureRef = ref()
const categoryAddPicturePreviewUrl = ref()

function onCategoryAddPictureChange() {
  const f = categoryAddPictureRef.value.files[0]
  categoryAddPicturePreviewUrl.value = f ? URL.createObjectURL(f) : ''
}

async function onCategoryAdd() {
  const formData = new FormData()
  formData.set('name', categoryToAdd.value.name)
  if (categoryAddPictureRef.value.files[0]) {
    formData.append('picture', categoryAddPictureRef.value.files[0])
  }

  await axios.post('/api/categories/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  categoryToAdd.value = { name: '' }
  categoryAddPictureRef.value.value = ''
  categoryAddPicturePreviewUrl.value = ''
  await fetchCategories()
}


async function onCategoryRemove(cat) {
  await axios.delete(`/api/categories/${cat.id}/`)
  await fetchCategories()
}


const categoryToEdit = ref({})
const categoryEditPictureRef = ref()
const categoryEditPicturePreviewUrl = ref()

function onCategoryEditClick(cat) {
  categoryToEdit.value = { ...cat }
  categoryEditPicturePreviewUrl.value = ''
}

function onCategoryEditPictureChange() {
  const f = categoryEditPictureRef.value.files[0]
  categoryEditPicturePreviewUrl.value = f ? URL.createObjectURL(f) : ''
}

async function onCategoryUpdate() {
  const formData = new FormData()
  formData.set('name', categoryToEdit.value.name)
  if (categoryEditPictureRef.value.files[0]) {
    formData.append('picture', categoryEditPictureRef.value.files[0])
  }

  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  categoryEditPictureRef.value.value = ''
  categoryEditPicturePreviewUrl.value = ''
  await fetchCategories()
}


const imageViewerUrl = ref('')

function openImageViewer(url) {
  imageViewerUrl.value = url
  const modal = new bootstrap.Modal(document.getElementById('imageViewerModal'))
  modal.show()
}


onBeforeMount(fetchCategories)
</script>

<template>
  <h1>Категории</h1>

  
  <form @submit.prevent="onCategoryAdd" class="row g-2 mb-3">
    <div class="col-auto">
      <input v-model="categoryToAdd.name" class="form-control" placeholder="Название" required />
    </div>
    <div class="col-auto">
      <input class="form-control" type="file" ref="categoryAddPictureRef" @change="onCategoryAddPictureChange" />
    </div>
    <div class="col-auto" v-if="categoryAddPicturePreviewUrl">
      <img :src="categoryAddPicturePreviewUrl" style="max-height: 60px;" />
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">Добавить</button>
    </div>
  </form>


  <ul class="list-group">
    <li v-for="cat in categories" :key="cat.id"
        class="list-group-item d-flex justify-content-between align-items-center">
      <div class="d-flex align-items-center gap-3">
        <img v-if="cat.picture" :src="cat.picture"
             style="max-height: 60px; cursor: pointer;"
             @click="openImageViewer(cat.picture)" />
        <span>{{ cat.name }}</span>
      </div>
      <div>
        <button class="btn btn-success btn-sm me-1" @click="onCategoryEditClick(cat)"
                data-bs-toggle="modal" data-bs-target="#editCategoryModal">✎</button>
        <button class="btn btn-danger btn-sm" @click="onCategoryRemove(cat)">✕</button>
      </div>
    </li>
  </ul>


  <div class="modal fade" id="editCategoryModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Редактировать категорию</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input v-model="categoryToEdit.name" class="form-control mb-2" />

          <img v-if="categoryToEdit.picture" :src="categoryToEdit.picture"
               style="max-height: 100px;" class="mb-2" />

          <input class="form-control mb-2" type="file"
                 ref="categoryEditPictureRef" @change="onCategoryEditPictureChange" />
          <img v-if="categoryEditPicturePreviewUrl" :src="categoryEditPicturePreviewUrl"
               style="max-height: 100px;" />
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button class="btn btn-primary" @click="onCategoryUpdate" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>


  <div class="modal fade" id="imageViewerModal" tabindex="-1">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Просмотр изображения</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body text-center">
          <img :src="imageViewerUrl" style="max-width: 100%; max-height: 75vh;" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>