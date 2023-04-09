<template>
  <Head title="Two-factor Confirmation" />

  <jet-authentication-card>
    <template #logo>
      <jet-authentication-card-logo />
    </template>

    <div class="card-body">

      <div class="mb-3">
        <template v-if="! recovery">
          Please confirm access to your account by entering the authentication code provided by your authenticator application.
        </template>

        <template v-else>
          Please confirm access to your account by entering one of your emergency recovery codes.
        </template>
      </div>

      <jet-validation-errors class="mb-3" />

      <form @submit.prevent="submit">
        <div class="mb-3" v-if="! recovery">
          <jet-label for="code" value="Code" />
          <jet-input ref="code" id="code" type="text" inputmode="numeric" v-model="form.code" autofocus autocomplete="one-time-code" />
        </div>

        <div class="mb-3" v-else>
          <jet-label for="recovery_code" value="Recovery Code" />
          <jet-input ref="recovery_code" id="recovery_code" type="text" v-model="form.recovery_code" autocomplete="one-time-code" />
        </div>

        <div class="d-flex justify-content-end mt-3">
          <button type="button" class="btn btn-outline-secondary" @click.prevent="toggleRecovery">
            <template v-if="! recovery">
              Use a recovery code
            </template>

            <template v-else>
              Use an authentication code
            </template>
          </button>

          <jet-button :class="{ 'text-white-50': form.processing }" :disabled="form.processing">
            <div v-show="form.processing" class="spinner-border spinner-border-sm" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>

            Log in
          </jet-button>
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
    JetValidationErrors,
  },

  data() {
    return {
      recovery: false,
      form: this.$inertia.form({
        code: '',
        recovery_code: '',
      })
    }
  },

  methods: {
    toggleRecovery() {
      this.recovery ^= true

      this.$nextTick(() => {
        if (this.recovery) {
          this.$refs.recovery_code.focus()
          this.form.code = '';
        } else {
          this.$refs.code.focus()
          this.form.recovery_code = ''
        }
      })
    },

    submit() {
      this.form.post(this.route('two-factor.login'))
    }
  }
})
</script>
