import UserIndex from "../pages/Users/UserIndex.vue";
import UserShow from "../pages/Users/UserShow.vue";

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
    {
        path: '/users/:id',
        name: 'user.show',
        component: UserShow,
        meta: {
            auth: true,
            permissions: ['user.view'],
        },
    },
]