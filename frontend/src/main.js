import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import Vuelidate from "vuelidate";
import { VueMaskDirective } from "v-mask";
import { createProvider } from "./vue-apollo";

Vue.directive("mask", VueMaskDirective);

Vue.use(Vuelidate);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  apolloProvider: createProvider(),
  render: h => h(App)
}).$mount("#app");
