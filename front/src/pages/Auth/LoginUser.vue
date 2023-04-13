<template>
  <jet-authentication-card>
    <template #logo>
      <jet-authentication-card-logo />
    </template>

    <div class="card-body">
      <div v-if="status" class="alert alert-success mb-3 rounded-0" role="alert">
        {{ status }}
      </div>

      <form @submit.prevent="submit">
        <div class="mb-3">
          <jet-label for="username" :value="$t('login.username')" />
          <jet-input id="username" type="username" v-model="username" required autofocus />
        </div>

        <div class="mb-3">
          <jet-label for="password" :value="$t('login.password')" />
          <jet-input id="password" type="password" v-model="password" required autocomplete="current-password" />
        </div>

        <div class="mb-0">
          <div class="d-flex justify-content-between align-items-baseline">
            <!-- <Link v-if="canResetPassword" :href="route('password.request')" class="text-muted me-3">
            Esqueceu sua senha?
            </Link> -->
            <div class="col-auto"><lang-change /></div>

            <jet-button class="ms-4" :class="{ 'text-white-50': loading }" :disabled="loading">
              <div v-show="loading" class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              Entrar
            </jet-button>
          </div>
        </div>
      </form>
    </div>
  </jet-authentication-card>
</template>

<script>
import { defineComponent } from 'vue'
import JetAuthenticationCard from '@/components/AuthenticationCard.vue'
import JetAuthenticationCardLogo from '@/components/AuthenticationCardLogo.vue'
import JetButton from '@/components/Button.vue'
import JetInput from '@/components/Input.vue'
import JetLabel from '@/components/Label.vue'
import LangChange from '@/components/LangChange.vue'

export default defineComponent({
  components: {
    JetAuthenticationCard,
    JetAuthenticationCardLogo,
    JetButton,
    JetInput,
    JetLabel,
    LangChange,
  },
  data() {
    return {
      username: '',
      password: '',
      status: '',
      loading: false
    }
  },

  methods: {
    submit() {

    }
  }
})
</script>
