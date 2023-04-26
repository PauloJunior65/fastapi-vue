
<template>
  <button @click="teste">teste</button>
  <router-view />
</template>

<script>
import { defineComponent } from "vue";
import { mapState } from "pinia";
import { sharedStore } from "./stores/shared";

export default defineComponent({
  computed: {
    ...mapState(sharedStore, ["isSupported", "memory"]),
  },
  methods: {
    teste() {
      console.log(this.isSupported, this.memory);
    },
  },
});
</script>