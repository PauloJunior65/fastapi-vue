import UserIndex from "../pages/Users/UserIndex.vue";

export default [
    {
        path: '/users',
        name: 'user.index',
        component: UserIndex,
        meta: {
            auth: true,
            permissions: ['user.view'],
        },
    },
]