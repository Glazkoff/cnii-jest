<template>
  <v-app id="app">
    <AppBar @change-drawer="changeDrawer"></AppBar>
    <v-navigation-drawer v-model="drawer" fixed temporary>
      <AppNavDrawer></AppNavDrawer>
    </v-navigation-drawer>
    <v-main>
      <v-container fill-height v-if="isAppLoading">
        <v-layout align-center="align-center" justify-center="justify-center">
          <v-progress-circular
            indeterminate
            :size="70"
            :width="7"
            color="primary"
          ></v-progress-circular>
        </v-layout>
      </v-container>
      <router-view v-else></router-view>
    </v-main>
  </v-app>
</template>

<script>
import AppBar from "@/components/global/AppBar.vue";
import AppNavDrawer from "@/components/global/AppNavDrawer.vue";

export default {
  name: "Main",
  components: {
    AppBar,
    AppNavDrawer
  },
  data() {
    return {
      drawer: false
    };
  },
  methods: {
    changeDrawer() {
      this.drawer = !this.drawer;
    }
  },
  computed: {
    isAppLoading() {
      return this.$store.state.loading;
    }
  }
};
</script>

<style lang="scss" scoped></style>
