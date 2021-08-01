import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import Vuelidate from "vuelidate";
import { VueMaskDirective } from "v-mask";
import { createProvider } from "./vue-apollo";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.directive("mask", VueMaskDirective);

Vue.use(VueAxios, axios);
Vue.use(Vuelidate);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  apolloProvider: createProvider(),
  render: h => h(App)
}).$mount("#app");
