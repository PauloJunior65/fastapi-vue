<template>
  <app-layout title="Dashboard">
    <template #header>
      <h2 class="h4 font-weight-bold">
        Dashboard
      </h2>
    </template>
    <font-awesome-icon icon="fa-solid fa-user-secret" />
    <welcome />
  </app-layout>
</template>

<script>
import { defineComponent } from "vue"
import Welcome from "../components/Welcome.vue"

export default defineComponent({
  components: {
    Welcome
  }
});
</script>
  
