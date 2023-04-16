<template>
    <app-layout :title="$t('users.title')">
        <template #header>
            <h2 class="h4 font-weight-bold">
                {{ $t('users.title') }}
            </h2>
        </template>
        <div class="card border m-1">
            <div class="card-header">
                <div class="row">
                    <div class="col-auto">
                        <button type="button" class="btn btn-sm btn-success">
                            {{ $t('users.button_new') }}
                        </button>
                    </div>
                    <div class="col-auto">
                        <div class="input-group input-group-sm mb-3">
                            <label class="input-group-text">{{ $t('users.show') }}</label>
                            <select class="form-select" v-model="size">
                                <option value="10">10</option>
                                <option value="50">50</option>
                                <option value="100">100</option>
                                <option value="1000">1000</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="input-group input-group-sm mb-3">
                            <label class="input-group-text">{{ $t('users.order') }}</label>
                            <select class="form-select" v-model="order">
                                <option :value="['id', 'asc']">{{ $t('users.order1') }}</option>
                                <option :value="['name', 'asc']">{{ $t('users.order2') }}</option>
                                <option :value="['email', 'asc']">{{ $t('users.order3') }}</option>
                                <option :value="['id', 'desc']">{{ $t('users.order1') }} DESC</option>
                                <option :value="['name', 'desc']">{{ $t('users.order2') }} DESC</option>
                                <option :value="['email', 'desc']">{{ $t('users.order3') }} DESC</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="input-group input-group-sm mb-3">
                            <label class="input-group-text">{{ $t('users.group') }}</label>
                            <select class="form-select">
                                <option value="">{{ $t('users.group_all') }}</option>
                                <option v-for="item in groups" :key="item" :value="item.id">{{ item.name }}</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="input-group input-group-sm mb-3">
                            <span class="input-group-text">{{ $t('users.pesquisa') }}</span>
                            <input type="text" class="form-control" :placeholder="$t('users.pesquisa_placeholder')"
                                v-model="name">
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col" class="text-center">ID</th>
                            <th scope="col" class="text-center">{{ $t('users.nome') }}</th>
                            <th scope="col" class="text-center">{{ $t('users.email') }}</th>
                            <th scope="col" class="text-center">{{ $t('users.group') }}</th>
                            <th scope="col" class="text-center">{{ $t('users.ative') }}</th>
                            <th scope="col" class="text-center">{{ $t('users.admin') }}</th>
                            <th scope="col" class="text-center">{{ $t('users.join') }}</th>
                            <th scope="col" class="text-center">{{ $t('users.option') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in items" :key="item">
                            <th scope="row">{{ item.id }}</th>
                            <td class="align-middle text-center">
                                {{ item.name }}
                            </td>
                            <td class="align-middle text-center">
                                {{ item.email }}
                            </td>
                            <td class="align-middle text-center" @mouseenter="item.display_groups = true"
                                @mouseleave="item.display_groups = false">
                                <template v-if="item.display_groups">
                                    <ul>
                                        <li v-for="group in item.groups" :key="group.id">
                                            {{ group.name }}
                                        </li>
                                    </ul>
                                </template>
                                <template v-else>
                                    {{ item.groups.length }} {{ $t('users.group') }}
                                </template>
                            </td>
                            <td class="align-middle text-center">
                                {{ item.is_active }}
                            </td>
                            <td class="align-middle text-center">
                                {{ item.is_superuser }}
                            </td>
                            <td class="align-middle text-center">
                                {{ item.date_joined != null ? item.date_joined : '-' }}
                            </td>
                            <td>
                                <div class="btn-group btn-group-sm" role="group">
                                    <button type="button" class="btn btn-outline-primary" :title="$t('users.option.show')">
                                        <font-awesome-icon icon="fa-solid fa-eye" />
                                    </button>
                                    <button type="button" class="btn btn-outline-warning" :title="$t('users.option.edit')">
                                        <font-awesome-icon icon="fa-solid fa-pen-to-square" />
                                    </button>
                                    <button type="button" class="btn btn-outline-danger" :title="$t('users.option.delete')">
                                        <font-awesome-icon icon="fa-solid fa-trash-can" />
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="card-body">
                <!-- <pagination :links="list.links" /> -->
            </div>
        </div>
    </app-layout>
</template>

<script>
import { defineComponent } from "vue";
import AppLayout from "@/Layouts/AppLayout.vue";
// import Pagination from "@/Components/Pagination.vue";
import { mapActions, mapWritableState } from "pinia";
import { authStore } from "../../stores/auth";
import { sharedStore } from "../../stores/shared";
import { api, exceptions } from "../../api";

export default defineComponent({
    components: {
        AppLayout,
        // Pagination,
    },
    data() {
        return {
            groups: [],
            items: [],
            total: 1,
            page: 1,
            pages: 1,

            group_selected: '',
            order: ['name', 'asc'],
            name: '',
        };
    },
    async mounted() {
        try {
            let res = await api().get('users/init');
            this.groups = res.data;
            this.load();
        } catch (error) {
            exceptions(error);
        }
    },
    computed: {
        ...mapWritableState(sharedStore, {
            size: 'sizePerPage',
        }),
    },
    methods: {
        ...mapActions(authStore, ['perms']),
        async load() {
            try {
                let res = await api().get('users');
                res.data.items = res.data.items.map((item) => {
                    item.display_groups = false;
                    return item;
                });
                Object.assign(this, res.data);
            } catch (error) {
                exceptions(error);
            }
        },
    },
});
</script>
