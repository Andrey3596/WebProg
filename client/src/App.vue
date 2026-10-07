<script setup>
</script>

<template>
  
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Кафе</a>

      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/profiles">Профили</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/categories">Категории</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/dishes">Блюда</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/orders">Заказы</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/orderitems">Позиции заказа</router-link>
        </li>
      </ul>

      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
            Пользователь
          </a>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item" href="/admin">Админка</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </nav>

  
  <div class="container mt-4">
    <router-view />
  </div>
</template>

<style scoped>
</style>