<template>
  <v-app-bar app color="white">
    <v-container class="py-0 fill-height">
      <v-app-bar-nav-icon
        @click="changeDrawer"
        class="mr-2"
      ></v-app-bar-nav-icon>
      <v-toolbar-title>ЦНИИ Русского жестового языка </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text> Подать заявку </v-btn>
      <v-btn to="/login" v-if="!isAuthenticated">Войти</v-btn>
      <v-btn text v-if="isAuthenticated" @click="logOut">Выйти</v-btn>
    </v-container>
  </v-app-bar>
</template>

<script>
export default {
  name: "AppBar",
  data() {
    return {};
  },
  methods: {
    changeDrawer() {
      this.$emit("change-drawer");
    },
    logOut() {
      this.$store.dispatch("LOG_OUT").then(
        () => {
          this.$router.push("/login");
        },
        err => {
          console.log(err);
        }
      );
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    }
  }
};
</script>

<style lang="scss" scoped></style>
