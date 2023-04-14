
<template>
  <router-view />
</template>

<script>
import { defineComponent } from "vue";
import { sharedStore } from "./stores/shared";

export default defineComponent({
  mounted() {
    const shared = sharedStore();
    shared.$router = this.$router;
  },
});
</script>