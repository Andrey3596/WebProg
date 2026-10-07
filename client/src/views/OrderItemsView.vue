<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const orderItems = ref([])
const orders = ref([])
const dishes = ref([])

async function fetchOrderItems() {
  const r = await axios.get('/api/orderitems/')
  orderItems.value = r.data
}

async function fetchOrders() {
  const r = await axios.get('/api/orders/')
  orders.value = r.data
}

async function fetchDishes() {
  const r = await axios.get('/api/dishes/')
  dishes.value = r.data
}


const itemToAdd = ref({ order: '', dish_id: '', quantity: 1, price: '' })

async function onItemAdd() {
  await axios.post('/api/orderitems/', {
    order: itemToAdd.value.order,
    dish_id: itemToAdd.value.dish_id,
    quantity: itemToAdd.value.quantity,
    price: itemToAdd.value.price,
  })
  itemToAdd.value = { order: '', dish_id: '', quantity: 1, price: '' }
  await fetchOrderItems()
}


async function onItemRemove(item) {
  await axios.delete(`/api/orderitems/${item.id}/`)
  await fetchOrderItems()
}


const itemToEdit = ref({})

function onItemEditClick(item) {
  itemToEdit.value = {
    id: item.id,
    order: item.order,
    dish_id: item.dish ? item.dish.id : '',
    quantity: item.quantity,
    price: item.price,
  }
}

async function onItemUpdate() {
  await axios.put(`/api/orderitems/${itemToEdit.value.id}/`, {
    order: itemToEdit.value.order,
    dish_id: itemToEdit.value.dish_id,
    quantity: itemToEdit.value.quantity,
    price: itemToEdit.value.price,
  })
  await fetchOrderItems()
}


onBeforeMount(async () => {
  await fetchOrders()
  await fetchDishes()
  await fetchOrderItems()
})
</script>

<template>
  <h1>Позиции заказа</h1>


  <form @submit.prevent="onItemAdd" class="row g-2 mb-3">
    <div class="col">
      <select v-model="itemToAdd.order" class="form-select" required>
        <option value="" disabled>Заказ</option>
        <option v-for="o in orders" :key="o.id" :value="o.id">Заказ #{{ o.id }}</option>
      </select>
    </div>
    <div class="col">
      <select v-model="itemToAdd.dish_id" class="form-select" required>
        <option value="" disabled>Блюдо</option>
        <option v-for="d in dishes" :key="d.id" :value="d.id">{{ d.name }}</option>
      </select>
    </div>
    <div class="col">
      <input v-model="itemToAdd.quantity" type="number" class="form-control" placeholder="Кол-во" />
    </div>
    <div class="col">
      <input v-model="itemToAdd.price" class="form-control" placeholder="Цена" />
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">Добавить</button>
    </div>
  </form>


  <table class="table table-striped">
    <thead>
      <tr>
        <th>ID</th>
        <th>Заказ</th>
        <th>Блюдо</th>
        <th>Кол-во</th>
        <th>Цена</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in orderItems" :key="item.id">
        <td>{{ item.id }}</td>
        <td>#{{ item.order }}</td>
        <td>{{ item.dish ? item.dish.name : '—' }}</td>
        <td>{{ item.quantity }}</td>
        <td>{{ item.price }}</td>
        <td>
          <button class="btn btn-success btn-sm me-1" @click="onItemEditClick(item)"
                  data-bs-toggle="modal" data-bs-target="#editItemModal">✎</button>
          <button class="btn btn-danger btn-sm" @click="onItemRemove(item)">✕</button>
        </td>
      </tr>
    </tbody>
  </table>


  <div class="modal fade" id="editItemModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Редактировать позицию</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <select v-model="itemToEdit.order" class="form-select mb-2">
            <option v-for="o in orders" :key="o.id" :value="o.id">Заказ #{{ o.id }}</option>
          </select>
          <select v-model="itemToEdit.dish_id" class="form-select mb-2">
            <option v-for="d in dishes" :key="d.id" :value="d.id">{{ d.name }}</option>
          </select>
          <input v-model="itemToEdit.quantity" type="number" class="form-control mb-2" placeholder="Кол-во" />
          <input v-model="itemToEdit.price" class="form-control" placeholder="Цена" />
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button class="btn btn-primary" @click="onItemUpdate" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>