<template>
    <app-layout :title="$t('users.title.show')">
        <template #header>
            <h2 class="h4 font-weight-bold">
                {{ $t('users.title.show') }}
            </h2>
        </template>
        <div class="card border m-1">
            <div class="card-header">
                <div class="row">
                    <div class="col-auto">
                        <h3>{{ $t('users.title.show') }}</h3>
                    </div>
                    <div class="col-auto">
                        <div class="row">

                        </div>
                    </div>
                </div>
            </div>
            <div class="card-body">

            </div>
        </div>
    </app-layout>
</template>

<script>
import { defineComponent } from "vue";
import AppLayout from "@/Layouts/AppLayout.vue";
import { mapActions } from "pinia";
import { authStore } from "../../stores/auth";
import { api, exceptions } from "../../api";

export default defineComponent({
    components: {
        AppLayout,
    },
    data() {
        return {
            id: 1,
            username: "",
            name: "",
            email: "",
            is_active: true,
            is_superuser: true,
            date_joined: null,
            created_at: "",
            updated_at: "",
            groups: []
        };
    },
    async mounted() {
        try {
            if ('user' in history.state) {
                Object.assign(this, JSON.parse(history.state.user));
            } else {
                let res = await api().get('users/' + this.$route.params.id);
                Object.assign(this, res.data);
            }
        } catch (error) {
            exceptions(error);
        }
    },
    computed: {
    },
    methods: {
        ...mapActions(authStore, ['perms']),
    },
});
</script>
