import Vue from "vue";
import Vuex from "vuex";
import jwt_decode from "jwt-decode";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    access_token: null,
    refresh_token: localStorage.getItem("t") || null,
    first_path: null,
    loading: false
  },
  getters: {
    decoded: state => {
      const access_token = state.access_token;
      if (access_token) {
        const decoded = jwt_decode(access_token);
        return decoded;
      } else {
        return null;
      }
    },
    user_id: state => {
      const access_token = state.access_token;
      if (access_token) {
        const decoded = jwt_decode(access_token);
        return decoded.user_id;
      } else {
        return null;
      }
    },
    isAuthenticated: state => {
      return state.access_token !== null && state.refresh_token !== null;
    }
  },
  mutations: {
    SET_ACCESS_TOKEN(state, token) {
      state.access_token = token;
    },
    SET_REFRESH_TOKEN(state, token) {
      localStorage.setItem("t", token);
      state.refresh_token = token;
    },
    START_APP_LOADING(state) {
      state.loading = true;
    },
    STOP_APP_LOADING(state) {
      state.loading = false;
    },
    SET_FIRST_PATH(state, firstPath) {
      state.firstPath = firstPath;
    }
  },
  actions: {
    LOG_IN(store, data) {
      return new Promise((resolve, reject) => {
        try {
          axios({
            url: "/api/auth/login/",
            method: "POST",
            data
          })
            .then(resp => {
              store.commit("SET_REFRESH_TOKEN", resp.data.refresh_token);
              store.commit("SET_ACCESS_TOKEN", resp.data.access_token);
              resolve(resp.data);
            })
            .catch(err => {
              reject(err.response.data);
            });
        } catch (error) {
          reject(error);
        }
      });
    },
    SIGN_UP(store, data) {
      store.loading = true;
      return new Promise((resolve, reject) => {
        try {
          axios({
            url: "/api/auth/registration/",
            method: "POST",
            data
          })
            .then(resp => {
              store.loading = false;
              resolve(resp.data);
            })
            .catch(err => {
              store.loading = false;
              reject(err.response.data);
            });
        } catch (error) {
          store.loading = false;
          reject(error);
        }
      });
    },
    REFRESH_TOKEN(store) {
      return new Promise((resolve, reject) => {
        try {
          axios({
            url: "/api/auth/token/refresh/",
            method: "POST",
            data: {
              token: store.refresh_token
            }
          })
            .then(resp => {
              store.commit("SET_ACCESS_TOKEN", resp.data.access);
              resolve(resp.data);
            })
            .catch(err => {
              localStorage.clear("t");
              reject(err.response.data);
            });
        } catch (error) {
          reject(error);
        }
      });
    },
    LOG_OUT(store) {
      return new Promise((resolve, reject) => {
        try {
          axios({
            url: "/api/auth/logout/",
            method: "POST",
            data: {}
          })
            .then(resp => {
              store.commit("SET_REFRESH_TOKEN", null);
              store.commit("SET_ACCESS_TOKEN", null);
              localStorage.clear("t");
              resolve(resp.data);
            })
            .catch(err => {
              localStorage.clear("t");
              reject(err.response.data);
            });
        } catch (error) {
          reject(error);
        }
      });
    }
  },
  modules: {}
});
