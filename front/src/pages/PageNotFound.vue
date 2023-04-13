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
                                <h6>{{ mesage }}</h6>
                            </div>
                            <div class="card-body">
                                <div class="row justify-content-between">
                                    <div class="col-auto">
                                        <router-link class="btn btn-sm btn-primary" to="/">
                                            {{ $t("error.back") }}
                                        </router-link>
                                    </div>
                                    <div class="col-auto">
                                        <button class="btn btn-sm btn-primary" @click="reset">
                                            {{ $t("error.reload") }}
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
export default defineComponent({
    data() {
        let code = (history.state.code != undefined) ? history.state.code : 404;
        let mesage = history.state.mesage || "";
        document.title = `${import.meta.env.VITE_TITLE} | ${code}`;
        if (mesage == "") {
            switch (code) {
                case 500:
                    mesage = this.$t("error.500");
                    break;
                case 403:
                    mesage = this.$t("error.403");
                    break;
                case 0:
                    mesage = this.$t("error.0");
                    break;
                default:
                    mesage = this.$t("error.404");
                    break;
            }
        }
        return {
            code: code,
            mesage: mesage,
            loadLoop: null,
        };
    },
    mounted() {
        this.loadLoop = setInterval(() => this.reset(), 30000);
    },
    beforeUnmount() {
        if (this.loadLoop != null) clearInterval(this.loadLoop);
    },
    methods: {
        reset() {
            window.location.reload(true);
        }
    },
});
</script>