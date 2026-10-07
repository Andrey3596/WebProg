<script setup>
import { computed, onBeforeMount, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const dishes = ref([]);


async function fetchDishes() {
    loading.value = true;
    const r = await axios.get("/api/dishes/");
    console.log(r.data)
    dishes.value = r.data;
    loading.value = false;
    
}
async function onLoadClick() {
    await fetchDishes();
}

onBeforeMount(async () => {
    await fetchDishes();
})
</script>


<template>

    <div v-for="item in dishes">
        {{ item.name }}
    </div>


    <button @click="onLoadClick">Загрузить</button>
</template>

<style scoped>
</style>
