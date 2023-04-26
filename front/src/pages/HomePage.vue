<template>
  <app-layout :title="$t('layout.home')">
    <template #header>
      <h2 class="h4 font-weight-bold">
        {{ $t('layout.home') }}
      </h2>
    </template>
    <font-awesome-icon icon="fa-regular fa-circle-xmark" />
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
  
