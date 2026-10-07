<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'


const dishes = ref([])
const categories = ref([])

async function fetchDishes() {
  const r = await axios.get('/api/dishes/')
  dishes.value = r.data
}

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}


const dishToAdd = ref({ name: '', description: '', price: '', category_id: '' })
const dishAddPictureRef = ref()
const dishAddPicturePreviewUrl = ref()

function onDishAddPictureChange() {
  const f = dishAddPictureRef.value.files[0]
  dishAddPicturePreviewUrl.value = f ? URL.createObjectURL(f) : ''
}

async function onDishAdd() {
  const formData = new FormData()
  formData.set('name', dishToAdd.value.name)
  formData.set('description', dishToAdd.value.description)
  formData.set('price', dishToAdd.value.price)
  formData.set('category_id', dishToAdd.value.category_id)
  if (dishAddPictureRef.value.files[0]) {
    formData.append('picture', dishAddPictureRef.value.files[0])
  }

  await axios.post('/api/dishes/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  dishToAdd.value = { name: '', description: '', price: '', category_id: '' }
  dishAddPictureRef.value.value = ''
  dishAddPicturePreviewUrl.value = ''
  await fetchDishes()
}


async function onDishRemove(dish) {
  await axios.delete(`/api/dishes/${dish.id}/`)
  await fetchDishes()
}


const dishToEdit = ref({})
const dishEditPictureRef = ref()
const dishEditPicturePreviewUrl = ref()

function onDishEditClick(dish) {
  dishToEdit.value = {
    id: dish.id,
    name: dish.name,
    description: dish.description,
    price: dish.price,
    category_id: dish.category ? dish.category.id : '',
    picture: dish.picture,
  }
  dishEditPicturePreviewUrl.value = ''
}

function onDishEditPictureChange() {
  const f = dishEditPictureRef.value.files[0]
  dishEditPicturePreviewUrl.value = f ? URL.createObjectURL(f) : ''
}

async function onDishUpdate() {
  const formData = new FormData()
  formData.set('name', dishToEdit.value.name)
  formData.set('description', dishToEdit.value.description)
  formData.set('price', dishToEdit.value.price)
  formData.set('category_id', dishToEdit.value.category_id)
  if (dishEditPictureRef.value.files[0]) {
    formData.append('picture', dishEditPictureRef.value.files[0])
  }

  await axios.put(`/api/dishes/${dishToEdit.value.id}/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  dishEditPictureRef.value.value = ''
  dishEditPicturePreviewUrl.value = ''
  await fetchDishes()
}


const imageViewerUrl = ref('')

function openImageViewer(url) {
  imageViewerUrl.value = url
  const modal = new bootstrap.Modal(document.getElementById('imageViewerModal'))
  modal.show()
}


onBeforeMount(async () => {
  await fetchCategories()
  await fetchDishes()
})
</script>

<template>
  <h1>Блюда</h1>


  <form @submit.prevent="onDishAdd" class="row g-2 mb-3">
    <div class="col">
      <input v-model="dishToAdd.name" class="form-control" placeholder="Название" required />
    </div>
    <div class="col">
      <input v-model="dishToAdd.description" class="form-control" placeholder="Описание" />
    </div>
    <div class="col">
      <input v-model="dishToAdd.price" class="form-control" placeholder="Цена" required />
    </div>
    <div class="col">
      <select v-model="dishToAdd.category_id" class="form-select" required>
        <option value="" disabled>Категория</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
    </div>
    <div class="col-auto">
      <input class="form-control" type="file" ref="dishAddPictureRef" @change="onDishAddPictureChange" />
    </div>
    <div class="col-auto" v-if="dishAddPicturePreviewUrl">
      <img :src="dishAddPicturePreviewUrl" style="max-height: 60px;" />
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">Добавить</button>
    </div>
  </form>


  <table class="table table-striped">
    <thead>
      <tr>
        <th>ID</th>
        <th>Фото</th>
        <th>Название</th>
        <th>Описание</th>
        <th>Цена</th>
        <th>Категория</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="dish in dishes" :key="dish.id">
        <td>{{ dish.id }}</td>
        <td>
          <img v-if="dish.picture" :src="dish.picture"
               style="max-height: 60px; cursor: pointer;"
               @click="openImageViewer(dish.picture)" />
        </td>
        <td>{{ dish.name }}</td>
        <td>{{ dish.description }}</td>
        <td>{{ dish.price }}</td>
        <td>{{ dish.category ? dish.category.name : '—' }}</td>
        <td>
          <button class="btn btn-success btn-sm me-1" @click="onDishEditClick(dish)"
                  data-bs-toggle="modal" data-bs-target="#editDishModal">✎</button>
          <button class="btn btn-danger btn-sm" @click="onDishRemove(dish)">✕</button>
        </td>
      </tr>
    </tbody>
  </table>


  <div class="modal fade" id="editDishModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Редактировать блюдо</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input v-model="dishToEdit.name" class="form-control mb-2" placeholder="Название" />
          <input v-model="dishToEdit.description" class="form-control mb-2" placeholder="Описание" />
          <input v-model="dishToEdit.price" class="form-control mb-2" placeholder="Цена" />
          <select v-model="dishToEdit.category_id" class="form-select mb-2">
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>

          <img v-if="dishToEdit.picture" :src="dishToEdit.picture"
               style="max-height: 100px;" class="mb-2" />

          <input class="form-control mb-2" type="file"
                 ref="dishEditPictureRef" @change="onDishEditPictureChange" />
          <img v-if="dishEditPicturePreviewUrl" :src="dishEditPicturePreviewUrl"
               style="max-height: 100px;" />
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button class="btn btn-primary" @click="onDishUpdate" data-bs-dismiss="modal">Сохранить</button>
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