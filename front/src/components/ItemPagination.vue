<template>
    <nav v-if="pages > 1">
        <ul class="pagination">
            <li class="page-item">
                <a class="page-link" aria-label="Previous" :class="{ disabled: page <= 1 }" @click="page -= 1">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
            <li class="page-item" v-for="p in pages" :key="p">
                <a class="page-link" @click="page = p">{{ p }}</a>
            </li>
            <li class="page-item">
                <a class="page-link" aria-label="Next" :class="{ disabled: page >= pages }" @click="page += 1">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        </ul>
    </nav>
</template>
<script>
export default {
    props: {
        modelValue: {
            type: Number,
            required: true,
        },
        pages: {
            type: Number,
            required: true,
        },
        load: {
            type: Function,
            default: async () => { },
        },
    },
    emits: ['update:modelValue'],
    computed: {
        page: {
            get() {
                return this.modelValue;
            },
            async set(value) {
                this.$emit('update:modelValue', value);
                await this.load();
            }
        }
    },
    methods: {
        async getLabel(label) {
            if (label.includes('&laquo;')) return '&laquo;';
            if (label.includes('&raquo;')) return '&raquo;';
            return label;
        }
    }
};
</script>
