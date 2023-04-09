<template>
  <Head title="Reset Password" />

  <jet-authentication-card>
    <template #logo>
      <jet-authentication-card-logo />
    </template>


    <div class="card-body">

      <jet-validation-errors class="mb-3" />

      <form @submit.prevent="submit">
        <div class="mb-3">
          <jet-label for="email" value="Email" />
          <jet-input id="email" type="email" v-model="form.email" required autofocus />
        </div>

        <div class="mb-3">
          <jet-label for="password" value="Password" />
          <jet-input id="password" type="password" v-model="form.password" required autocomplete="new-password" />
        </div>

        <div class="mb-3">
          <jet-label for="password_confirmation" value="Confirmação de senha" />
          <jet-input id="password_confirmation" type="password" v-model="form.password_confirmation" required autocomplete="new-password" />
        </div>

        <div class="mb-0">
          <div class="d-flex justify-content-end">
            <jet-button :class="{ 'text-white-50': form.processing }" :disabled="form.processing">
              <div v-show="form.processing" class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              
              Reset Password
            </jet-button>
          </div>
        </div>
      </form>
    </div>
  </jet-authentication-card>
</template>

<script>
import { defineComponent } from 'vue'
import { Head } from '@inertiajs/inertia-vue3'
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
    email: String,
    token: String,
  },

  data() {
    return {
      form: this.$inertia.form({
        token: this.token,
        email: this.email,
        password: '',
        password_confirmation: '',
      })
    }
  },

  methods: {
    submit() {
      this.form.post(this.route('password.update'), {
        onFinish: () => this.form.reset('password', 'password_confirmation'),
      })
    }
  }
})
</script>
