<template>
  <Head title="Esqueceu sua senha" />

  <jet-authentication-card>
    <template #logo>
      <jet-authentication-card-logo />
    </template>

    <div class="card-body">
      <div class="mb-2">
        Forgot your password? No problem. Just let us know your email address and we will email you a password reset link that will allow you to choose a new one.
      </div>

      <div v-if="status" class="alert alert-success" role="alert">
        {{ status }}
      </div>

      <jet-validation-errors class="mb-2" />

      <form @submit.prevent="submit">
        <div>
          <jet-label for="email" value="Email" />
          <jet-input id="email" type="email" v-model="form.email" required autofocus />
        </div>

        <div class="d-flex justify-content-end mt-4">
          <jet-button :class="{ 'text-white-50': form.processing }" :disabled="form.processing">
            <div v-show="form.processing" class="spinner-border spinner-border-sm" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            
            Email Password Reset Link
          </jet-button>
        </div>
      </form>
    </div>
  </jet-authentication-card>
</template>

<script>
import { defineComponent } from 'vue'
import { Head } from '@inertiajs/inertia-vue3';
import JetAuthenticationCard from '@/Components/AuthenticationCard.vue'
import JetAuthenticationCardLogo from '@/Components/AuthenticationCardLogo.vue'
import JetButton from '@/Components/Button.vue'
import JetInput from '@/Components/Input.vue'
import JetLabel from '@/Components/Label.vue'
import JetValidationErrors from '@/Components/ValidationErrors.vue'

export default defineComponent({
  components: {
    Head,
    JetAuthenticationCard,
    JetAuthenticationCardLogo,
    JetButton,
    JetInput,
    JetLabel,
    JetValidationErrors
  },

  props: {
    status: String
  },

  data() {
    return {
      form: this.$inertia.form({
        email: ''
      })
    }
  },

  methods: {
    submit() {
      this.form.post(this.route('password.email'))
    }
  }
})
</script>
