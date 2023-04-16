<template>
    <app-layout :title="$t('group.title_edit')">
        <template #header>
            <h2 class="h4 font-weight-bold">
                {{ $t('group.title_edit') }}
            </h2>
        </template>
        <div class="card border m-1">
            <div class="card-body">
                <form>
                    <div class="mb-3">
                        <label for="input-name" class="form-label">{{ $t('group.name') }}</label>
                        <input type="text" class="form-control" id="input-name">
                    </div>
                    <div class="row mb-3">
                        <div class="col" v-for="item in permissions">
                            <div class="card border m-2">
                                <div class="card-body py-0 pt-2">
                                    <h6>{{ item.name }}</h6>
                                </div>
                                <div class="card-body py-0 pb-2">
                                    <div class="form-check" v-for="perm in item.permissions">
  <input class="form-check-input" type="checkbox" value="">
  <label class="form-check-label">
    {{ perm.description }} ({{ perm.name }})
  </label>
</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
                {{ permissions }}
            </div>
        </div>
    </app-layout>
</template>

<script>
import { defineComponent } from "vue";
import AppLayout from "@/Layouts/AppLayout.vue";

export default defineComponent({
    props: {
        permissions: Array,
    },
    components: {
        AppLayout,
    },
    data() {
        return {
            order: 'name',
            search: '',
            show: 10,
        };
    },
    methods: {

    },
});
</script>
