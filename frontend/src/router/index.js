import Vue from "vue";
import VueRouter from "vue-router";
import store from "../store/index.js";

import Main from "../views/Main.vue";
import Auth from "@/components/auth/Auth.vue";
import LogIn from "@/components/auth/LogIn.vue";
import SignUp from "@/components/auth/SignUp.vue";
import UserStatusScreen from "@/components/users_screen/UserStatusScreen.vue";
import AttestableView from "@/components/users_screen/attestable/AttestableView.vue";

Vue.use(VueRouter);

const ifAuthenticated = (to, from, next) => {
  if (store.state.firstPath == null) {
    store.commit("SET_FIRST_PATH", to.path);
  }

  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/login");
};

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/");
};

const routes = [
  {
    path: "/",
    component: Main,
    children: [
      {
        path: "/login",
        component: Auth,
        beforeEnter: ifNotAuthenticated,
        children: [
          {
            path: "/",
            name: "LogIn",
            component: LogIn
          },
          {
            path: "/signup",
            name: "SignUp",
            component: SignUp
          }
        ]
      },
      {
        path: "/",
        beforeEnter: ifAuthenticated,
        component: UserStatusScreen,
        children: [
          {
            path: "/",
            component: AttestableView,
            name: "AttestableView"
          }
        ]
      }
    ]
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
