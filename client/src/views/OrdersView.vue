<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'


const orders = ref([])
const profiles = ref([])

const statuses = [
  { value: 'processing', label: 'В обработке' },
  { value: 'ready',      label: 'Готово' },
  { value: 'completed',  label: 'Завершён' },
  { value: 'cancelled',  label: 'Отменён' },
]

async function fetchOrders() {
  const r = await axios.get('/api/orders/')
  orders.value = r.data
}

async function fetchProfiles() {
  const r = await axios.get('/api/profiles/')
  profiles.value = r.data
}


const orderToAdd = ref({ user_id: '', status: 'processing', total_amount: '0.00' })

async function onOrderAdd() {
  await axios.post('/api/orders/', {
    user_id: orderToAdd.value.user_id,
    status: orderToAdd.value.status,
    total_amount: orderToAdd.value.total_amount,
  })
  orderToAdd.value = { user_id: '', status: 'processing', total_amount: '0.00' }
  await fetchOrders()
}


async function onOrderRemove(order) {
  await axios.delete(`/api/orders/${order.id}/`)
  await fetchOrders()
}


const orderToEdit = ref({})

function onOrderEditClick(order) {
  orderToEdit.value = {
    id: order.id,
    user_id: order.user ? order.user.id : '',
    status: order.status,
    total_amount: order.total_amount,
  }
}

async function onOrderUpdate() {
  await axios.put(`/api/orders/${orderToEdit.value.id}/`, {
    user_id: orderToEdit.value.user_id,
    status: orderToEdit.value.status,
    total_amount: orderToEdit.value.total_amount,
  })
  await fetchOrders()
}


onBeforeMount(async () => {
  await fetchProfiles()
  await fetchOrders()
})
</script>

<template>
  <h1>Заказы</h1>


  <form @submit.prevent="onOrderAdd" class="row g-2 mb-3">
    <div class="col">
      <select v-model="orderToAdd.user_id" class="form-select" required>
        <option value="" disabled>Пользователь</option>
        <option v-for="p in profiles" :key="p.id" :value="p.user.id">
          {{ p.user.username }}
        </option>
      </select>
    </div>
    <div class="col">
      <select v-model="orderToAdd.status" class="form-select">
        <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
      </select>
    </div>
    <div class="col">
      <input v-model="orderToAdd.total_amount" class="form-control" placeholder="Сумма" />
    </div>
    <div class="col-auto">
      <button class="btn btn-primary">Добавить</button>
    </div>
  </form>


  <table class="table table-striped">
    <thead>
      <tr>
        <th>ID</th>
        <th>Пользователь</th>
        <th>Дата</th>
        <th>Статус</th>
        <th>Сумма</th>
        <th>Позиции</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="order in orders" :key="order.id">
        <td>{{ order.id }}</td>
        <td>{{ order.user ? order.user.username : '—' }}</td>
        <td>{{ order.created_at }}</td>
        <td>{{ order.status }}</td>
        <td>{{ order.total_amount }}</td>
        <td>{{ order.items ? order.items.length : 0 }}</td>
        <td>
          <button class="btn btn-success btn-sm me-1" @click="onOrderEditClick(order)"
                  data-bs-toggle="modal" data-bs-target="#editOrderModal">✎</button>
          <button class="btn btn-danger btn-sm" @click="onOrderRemove(order)">✕</button>
        </td>
      </tr>
    </tbody>
  </table>


  <div class="modal fade" id="editOrderModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Редактировать заказ</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <select v-model="orderToEdit.user_id" class="form-select mb-2">
            <option v-for="p in profiles" :key="p.id" :value="p.user.id">
              {{ p.user.username }}
            </option>
          </select>
          <select v-model="orderToEdit.status" class="form-select mb-2">
            <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>
          <input v-model="orderToEdit.total_amount" class="form-control" placeholder="Сумма" />
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button class="btn btn-primary" @click="onOrderUpdate" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>