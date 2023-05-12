<template>
  <hr class="dropdown-divider">
  <h6 class="dropdown-header small text-muted">
    Status Application
  </h6>
  <template v-if="isSupported && memory">
    <template v-if="memory">
      <li class="dropdown-item px-4">Used: {{ size(memory.usedJSHeapSize) }}</li>
      <li class="dropdown-item px-4">Allocated: {{ size(memory.totalJSHeapSize) }}</li>
      <li class="dropdown-item px-4">Limit: {{ size(memory.jsHeapSizeLimit) }}</li>
    </template>
  </template>
  <template v-else>
    <li class="dropdown-item px-4">Your browser does not support performance memory API</li>
  </template>
</template>

<script>
import { defineComponent } from 'vue';
import { useMemory } from '@vueuse/core';

export default defineComponent({
  setup() {
    const { isSupported, memory } = useMemory();
    return { isSupported, memory };
  },
  methods: {
    size(v) {
      const kb = v / 1024 / 1024
      return `${kb.toFixed(2)} MB`
    }
  },
})
</script>