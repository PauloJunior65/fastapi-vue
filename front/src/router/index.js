import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/HomePage.vue'
import PageNotFound from '../pages/PageNotFound.vue'
import { authStore } from '../stores/auth';



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        auth: false,
        permissions: [],
      },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "error",
      component: PageNotFound,
      meta: {
        auth: false,
        permissions: [],
      },
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
});

router.beforeEach((to, from, next) => {
  const store = authStore();
  let auth = store.is_auth();
  let perm = store.perms(to.meta.perm)
  if (to.name == "login" && auth) {
    next({ name: "home" });
  } else if (to.meta.auth && !auth) {
    next({ name: "login" });
  } else if (to.meta.auth && !perm) {
    next({
      name: "error",
      params: {
        pathMatch: to.path.substring(1).split("/"),
      },
      state: {
        code: 403
      }
    });
  } else next();
});

export default router
