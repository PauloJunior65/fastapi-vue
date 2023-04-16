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
                        <!-- <Link :href="route('admin.groups.create')" type="button" class="btn btn-sm btn-primary">
                        {{ $t('groups.button_new') }}
                        </Link> -->
                    </div>
                    <div class="col-auto">
                        <div class="input-group input-group-sm mb-3">
                            <label class="input-group-text">{{ $t('users.show') }}</label>
                            <select class="form-select">
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
                            <select class="form-select">
                                <option value="id">{{ $t('users.order1') }}</option>
                                <option value="name">{{ $t('users.order2') }}</option>
                                <option value="email">{{ $t('users.order3') }}</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="input-group input-group-sm mb-3">
                            <span class="input-group-text">{{ $t('users.pesquisa') }}</span>
                            <input type="text" class="form-control" aria-label="Sizing example input">
                        </div>
                    </div>
                    <div class="col-auto">
                        <button type="button" class="btn btn-sm btn-primary">
                            {{ $t('users.button') }}
                        </button>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">{{ $t('users.nome') }}</th>
                            <th scope="col">{{ $t('users.email') }}</th>
                            <th scope="col">{{ $t('users.editar') }}</th>
                            <th scope="col">{{ $t('users.drop') }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- <tr v-for="item in list.data" :key="item">
                            <th scope="row">{{ item.id }}</th>
                            <td class="align-middle">
                                <img class="rounded-circle" width="32" height="32" :src="item.profile_photo_url"
                                    :alt="item.name" />
                                {{ item.name }}
                            </td>
                            <td class="align-middle">
                                {{ item.email }}
                            </td>
                            <td></td>
                            <td></td>
                        </tr> -->
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

export default defineComponent({
    components: {
        AppLayout,
        // Pagination,
    },
    data() {
        return {
            list: {},
            order: 'name',
            search: '',
            show: 10,
        };
    },
    methods: {

    },
});
</script>
