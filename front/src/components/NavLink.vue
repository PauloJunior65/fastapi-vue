<template>
  <li class="nav-item">
    <router-link class="nav-link" active-class="active font-weight-bolder" :to="{ name: name }">
      <slot></slot>
    </router-link>
  </li>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    name: {
      type: String,
      required: true
    }
  },
})
</script>
