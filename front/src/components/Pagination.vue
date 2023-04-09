<template>
    <nav v-if="links.length > 3">
        <ul class="pagination">
            <li  v-for="(link, p) in links" :key="p" class="page-item">
                <div v-if="link.url === null" class="page-link" v-html="getLabel(link.label)"/>
                <Link
                    v-else
                    class="page-link"
                    :href="link.url"
                    v-html="getLabel(link.label)"
                />
            </li>
        </ul>
    </nav>
</template>
<script>
import { Link } from "@inertiajs/inertia-vue3";
export default {
    components: {
        Link,
    },
    props: {
        links: Array,
    },
    methods:{
        getLabel(label){
            if (label.includes('&laquo;')) return '&laquo;';
            if (label.includes('&raquo;')) return '&raquo;';
            return label;
        }
    }
};
</script>
