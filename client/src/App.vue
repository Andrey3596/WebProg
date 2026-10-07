<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})


//КАТЕГОРИИ
const categories = ref([])
const categoryToAdd = ref({ name: '' })
const categoryToEdit = ref({})

async function fetchCategories() {
  const r = await axios.get('/api/categories/')
  categories.value = r.data
}

async function onCategoryAdd() {
  await axios.post('/api/categories/', { name: categoryToAdd.value.name })
  categoryToAdd.value = { name: '' }
  await fetchCategories()
}

async function onCategoryRemove(cat) {
  await axios.delete(`/api/categories/${cat.id}/`)
  await fetchCategories()
}

function onCategoryEditClick(cat) {
  categoryToEdit.value = { ...cat }
}

async function onCategoryUpdate() {
  await axios.put(`/api/categories/${categoryToEdit.value.id}/`, {
    name: categoryToEdit.value.name,
  })
  await fetchCategories()
}


//БЛЮДА

const dishes = ref([])
const dishToAdd = ref({ name: '', description: '', price: '', category_id: '' })
const dishToEdit = ref({})

async function fetchDishes() {
  const r = await axios.get('/api/dishes/')
  dishes.value = r.data
}

async function onDishAdd() {
  await axios.post('/api/dishes/', {
    name: dishToAdd.value.name,
    description: dishToAdd.value.description,
    price: dishToAdd.value.price,
    category_id: dishToAdd.value.category_id,
  })
  dishToAdd.value = { name: '', description: '', price: '', category_id: '' }
  await fetchDishes()
}

async function onDishRemove(dish) {
  await axios.delete(`/api/dishes/${dish.id}/`)
  await fetchDishes()
}

function onDishEditClick(dish) {
  dishToEdit.value = {
    id: dish.id,
    name: dish.name,
    description: dish.description,
    price: dish.price,
    category_id: dish.category ? dish.category.id : '',
  }
}

async function onDishUpdate() {
  await axios.put(`/api/dishes/${dishToEdit.value.id}/`, {
    name: dishToEdit.value.name,
    description: dishToEdit.value.description,
    price: dishToEdit.value.price,
    category_id: dishToEdit.value.category_id,
  })
  await fetchDishes()
}


//ЗАКАЗЫ
const orders = ref([])
const orderToAdd = ref({ user_id: '', status: 'processing', total_amount: '0.00' })
const orderToEdit = ref({})

const statuses = [
  { value: 'processing', label: 'В обработке' },
  { value: 'ready', label: 'Готово' },
  { value: 'completed', label: 'Завершён' },
  { value: 'cancelled', label: 'Отменён' },
]

async function fetchOrders() {
  const r = await axios.get('/api/orders/')
  orders.value = r.data
}

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


//ПОЗИЦИИ ЗАКАЗА

const orderItems = ref([])
const itemToAdd = ref({ order: '', dish_id: '', quantity: 1, price: '' })
const itemToEdit = ref({})

async function fetchOrderItems() {
  const r = await axios.get('/api/orderitems/')
  orderItems.value = r.data
}

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

//Загрузка старте
onBeforeMount(async () => {
  await fetchCategories()
  await fetchDishes()
  await fetchOrders()
  await fetchOrderItems()
})
</script>

<template>

  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid justify-content-between">
    <a class="navbar-brand" href="#">Кафе</a>

    <ul class="navbar-nav">
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          href="#"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          Пользователь
        </a>
        <ul class="dropdown-menu dropdown-menu-end">
          <li>
            <a class="dropdown-item" href="/admin">Админка</a>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</nav>

  <div class="container mt-4">
    <h1>Кафе — управление</h1>

    <!--КАТЕГОРИИ-->
    <h2 class="mt-4">Категории</h2>

    <form @submit.prevent="onCategoryAdd" class="row g-2 mb-3">
      <div class="col-auto">
        <input v-model="categoryToAdd.name" class="form-control" placeholder="Название" required />
      </div>
      <div class="col-auto">
        <button class="btn btn-primary">Добавить</button>
      </div>
    </form>

    <ul class="list-group mb-3">
      <li v-for="cat in categories" :key="cat.id" class="list-group-item d-flex justify-content-between">
        <span>{{ cat.name }}</span>
        <div>
          <button class="btn btn-success btn-sm me-1" @click="onCategoryEditClick(cat)"
                  data-bs-toggle="modal" data-bs-target="#editCategoryModal">✎</button>
          <button class="btn btn-danger btn-sm" @click="onCategoryRemove(cat)">✕</button>
        </div>
      </li>
    </ul>

    <!--БЛЮДА -->
    <h2 class="mt-5">Блюда</h2>

    <form @submit.prevent="onDishAdd" class="row g-2 mb-3">
      <div class="col"><input v-model="dishToAdd.name" class="form-control" placeholder="Название" required /></div>
      <div class="col"><input v-model="dishToAdd.description" class="form-control" placeholder="Описание" /></div>
      <div class="col"><input v-model="dishToAdd.price" class="form-control" placeholder="Цена" required /></div>
      <div class="col">
        <select v-model="dishToAdd.category_id" class="form-select" required>
          <option value="" disabled>Категория</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
      </div>
      <div class="col-auto"><button class="btn btn-primary">Добавить</button></div>
    </form>

    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>Название</th><th>Описание</th><th>Цена</th><th>Категория</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="dish in dishes" :key="dish.id">
          <td>{{ dish.id }}</td>
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

    <!--ЗАКАЗЫ -->
    <h2 class="mt-5">Заказы</h2>

    <form @submit.prevent="onOrderAdd" class="row g-2 mb-3">
      <div class="col"><input v-model="orderToAdd.user_id" class="form-control" placeholder="ID пользователя" required /></div>
      <div class="col">
        <select v-model="orderToAdd.status" class="form-select">
          <option v-for="s in statuses" :key="s.value" :value="s.value">{{ s.label }}</option>
        </select>
      </div>
      <div class="col"><input v-model="orderToAdd.total_amount" class="form-control" placeholder="Сумма" /></div>
      <div class="col-auto"><button class="btn btn-primary">Добавить</button></div>
    </form>

    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>Пользователь</th><th>Дата</th><th>Статус</th><th>Сумма</th><th></th></tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.id">
          <td>{{ order.id }}</td>
          <td>{{ order.user ? order.user.username : '—' }}</td>
          <td>{{ order.created_at }}</td>
          <td>{{ order.status }}</td>
          <td>{{ order.total_amount }}</td>
          <td>
            <button class="btn btn-success btn-sm me-1" @click="onOrderEditClick(order)"
                    data-bs-toggle="modal" data-bs-target="#editOrderModal">✎</button>
            <button class="btn btn-danger btn-sm" @click="onOrderRemove(order)">✕</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!--ПОЗИЦИИ ЗАКАЗА-->
    <h2 class="mt-5">Позиции заказа</h2>

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
      <div class="col"><input v-model="itemToAdd.quantity" type="number" class="form-control" placeholder="Кол-во" /></div>
      <div class="col"><input v-model="itemToAdd.price" class="form-control" placeholder="Цена" /></div>
      <div class="col-auto"><button class="btn btn-primary">Добавить</button></div>
    </form>

    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>Заказ</th><th>Блюдо</th><th>Кол-во</th><th>Цена</th><th></th></tr>
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
  </div>

  <!--МОДАЛЬНОЕ ОКНО: КАТЕГОРИЯ-->
  <div class="modal fade" id="editCategoryModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header"><h5 class="modal-title">Редактировать категорию</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input v-model="categoryToEdit.name" class="form-control" />
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button class="btn btn-primary" @click="onCategoryUpdate" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>

  <!--МОДАЛЬНОЕ ОКНО: БЛЮДО-->
  <div class="modal fade" id="editDishModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header"><h5 class="modal-title">Редактировать блюдо</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input v-model="dishToEdit.name" class="form-control mb-2" placeholder="Название" />
          <input v-model="dishToEdit.description" class="form-control mb-2" placeholder="Описание" />
          <input v-model="dishToEdit.price" class="form-control mb-2" placeholder="Цена" />
          <select v-model="dishToEdit.category_id" class="form-select">
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button class="btn btn-primary" @click="onDishUpdate" data-bs-dismiss="modal">Сохранить</button>
        </div>
      </div>
    </div>
  </div>

  <!--МОДАЛЬНОЕ ОКНО: ЗАКАЗ-->
  <div class="modal fade" id="editOrderModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header"><h5 class="modal-title">Редактировать заказ</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input v-model="orderToEdit.user_id" class="form-control mb-2" placeholder="ID пользователя" />
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

  <!--МОДАЛЬНОЕ ОКНО: ПОЗИЦИЯ -->
  <div class="modal fade" id="editItemModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header"><h5 class="modal-title">Редактировать позицию</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <input v-model="itemToEdit.order" class="form-control mb-2" placeholder="ID заказа" />
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
