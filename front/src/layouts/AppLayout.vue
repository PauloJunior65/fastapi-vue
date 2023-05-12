<template>
  <div>
    <nav class="navbar navbar-expand-md navbar-light bg-white border-bottom sticky-top">
      <div class="container-fluid">
        <!-- Logo -->
        <router-link class="navbar-brand me-4" :to="{ name: 'home' }">
          <ApplicationMark width="36" />
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <!-- Left Side Of Navbar -->
          <ul class="navbar-nav me-auto">
            <NavLink name="home">
              {{ $t('layout.home') }}
            </NavLink>
            <NavLink name="user.index">
              {{ $t('layout.users') }}
            </NavLink>
          </ul>
          <!-- Right Side Of Navbar -->
          <ul class="navbar-nav align-items-baseline">
            <!-- Language -->
            <div>
              <select class="form-select" v-model="$i18n.locale">
                <option v-for="locale in $i18n.availableLocales" :key="`locale-${locale}`" :value="locale">
                  {{ locale.toUpperCase().replace(/_/g, "-") }}
                </option>
              </select>
            </div>
            <!-- Authentication Links -->
            <Dropdown id="settingsDropdown">
              <template #trigger>
                {{ name }}
              </template>
              <template #content>
                <!-- Account Management -->
                <h6 class="dropdown-header small text-muted">
                  {{ $t('layout.account') }}
                </h6>
                <router-link class="dropdown-item px-4" :to="{ name: 'home' }">
                  {{ $t('layout.profile') }}
                </router-link>
                <hr class="dropdown-divider">
                <!-- Authentication -->
                <form @submit.prevent="logout">
                  <button type="submit" class="dropdown-item px-4">
                    {{ $t('layout.logout') }}
                  </button>
                </form>
                <MemoryUse />
              </template>
            </Dropdown>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Page Heading -->
    <header class="d-flex py-3 bg-white shadow-sm border-bottom">
      <div class="container-fluid">
        <slot name="header"></slot>
      </div>
    </header>

    <!-- Page Content -->
    <main class="container-fluid my-5">
      <slot></slot>
    </main>
  </div>
</template>

<script>
import { defineComponent } from "vue"
import ApplicationMark from '@/components/ApplicationMark.vue'
import Dropdown from '@/components/Dropdown.vue'
import NavLink from '@/components/NavLink.vue'
import MemoryUse from "@/components/MemoryUse.vue";
import { authStore } from "@/stores/auth"
import { mapActions, mapState } from "pinia";

export default defineComponent({
  props: {
    title: {
      type: String,
      default: ''
    },
  },
  components: {
    ApplicationMark,
    Dropdown,
    NavLink,
    MemoryUse
  },
  mounted() {
    this.setTitle();
  },
  watch: {
    $i18n: {
      handler() {
        this.setTitle();
      },
      deep: true
    }
  },
  computed: {
    ...mapState(authStore, ['name']),
  },
  methods: {
    ...mapActions(authStore, ['logout']),
    setTitle() {
      if (this.title.length > 0) {
        document.title = import.meta.env.VITE_TITLE + " | " + this.title;
      } else document.title = import.meta.env.VITE_TITLE;
      document.documentElement.setAttribute("lang", this.$i18n.locale.replace("_", "-"));
    }
  },
});
</script>
