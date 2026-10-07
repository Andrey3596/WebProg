<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const profiles = ref([])

const roleLabels = {
  0: 'Не определена',
  1: 'Сотрудник',
  2: 'Клиент',
}

async function fetchProfiles() {
  const r = await axios.get('/api/profiles/')
  profiles.value = r.data
}

onBeforeMount(fetchProfiles)
</script>

<template>
  <h1>Профили</h1>

  <table class="table table-striped mt-3">
    <thead>
      <tr>
        <th>ID</th>
        <th>Пользователь</th>
        <th>Роль</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="p in profiles" :key="p.id">
        <td>{{ p.id }}</td>
        <td>{{ p.user ? p.user.username : '—' }}</td>
        <td>{{ roleLabels[p.role] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
</style>