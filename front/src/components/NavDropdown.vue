<template>
  <li class="nav-item dropdown">
    <a :class="classes" role="button" data-bs-toggle="dropdown" aria-expanded="false">
      <slot name="trigger"></slot>
    </a>
    <div class="dropdown-menu animate">
      <slot name="content"></slot>
    </div>
  </li>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    active: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    classes() {
      return this.active
        ? 'nav-link active font-weight-bolder'
        : 'nav-link'
    }
  }
})
</script>
