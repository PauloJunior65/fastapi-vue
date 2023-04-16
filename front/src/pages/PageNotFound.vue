<template>
    <section>
        <div class="page-header section-height-75">
            <div class="container">
                <div class="row py-1">
                    <div class="col-xl-6 col-lg-7 col-md-8 col-sm-12 mx-auto">
                        <div class="card card-plain mt-8 shadow">
                            <div class="card-header pb-0 text-left bg-transparent">
                                <h3>{{ $t("error.err") }} {{ code }}</h3>
                            </div>
                            <div class="card-body">
                                <h6>{{ message }}</h6>
                            </div>
                            <div class="card-body">
                                <div class="row justify-content-between">
                                    <div class="col-auto">
                                        <router-link class="btn btn-sm btn-primary" :to="{ name: 'home' }" v-if="auth">
                                            {{ $t("error.back") }}
                                        </router-link>
                                        <router-link class="btn btn-sm btn-primary" :to="{ name: 'login' }" v-else>
                                            {{ $t("error.login") }}
                                        </router-link>
                                    </div>
                                    <div class="col-auto">
                                        <button class="btn btn-sm btn-primary" @click="reset(true)">
                                            {{ $t("error.reload") }} <span v-if="duration > 0">({{ duration }})</span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
  
<script>
import { defineComponent } from "vue"
import { mapState } from "pinia";
import { authStore } from "../stores/auth";
export default defineComponent({
    data() {
        let code = (history.state.code != undefined) ? history.state.code : 404;
        let message = history.state.message || "";
        document.title = `${import.meta.env.VITE_TITLE} | ${code}`;
        if (message == "") {
            switch (code) {
                case 401:
                    message = this.$t("error.401");
                    break;
                case 403:
                    message = this.$t("error.403");
                    break;
                case 422:
                    message = this.$t("error.422");
                    break;
                case 500:
                    message = this.$t("error.500");
                    break;
                default:
                    message = this.$t("error.404");
                    break;
            }
        }
        return {
            code: code,
            message: message,
            duration: 300,
            loadLoop: null,
        };
    },
    computed: {
        ...mapState(authStore, ['auth'])
    },
    mounted() {
        this.loadLoop = setInterval(() => this.reset(), 1000);
    },
    beforeUnmount() {
        if (this.loadLoop != null) clearInterval(this.loadLoop);
    },
    methods: {
        reset(reset = false) {
            if (this.duration > 0) this.duration--;
            if (reset || this.duration == 0) window.location.reload(true);
        }
    },
});
</script>