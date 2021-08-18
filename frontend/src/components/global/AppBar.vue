<template>
  <v-app-bar app color="white">
    <v-container class="py-0 fill-height">
      <v-app-bar-nav-icon
        @click="changeDrawer"
        class="mr-2 d-flex d-sm-none"
      ></v-app-bar-nav-icon>
      <v-avatar size="40" class="mr-2">
        <img
          src="../../assets/logo.svg"
          alt="Лого ЦНИИ Русского жестового языка"
        />
      </v-avatar>
      <v-toolbar-title class="d-none d-sm-none d-md-flex">
        ЦНИИ Русского жестового языка
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn class="d-none d-sm-flex" text to="/" v-if="isAuthenticated">
        Список заявок
      </v-btn>
      <v-btn class="d-none d-sm-flex" to="/login" v-if="!isAuthenticated" text>
        Войти
      </v-btn>
      <v-btn class="d-none d-sm-flex" to="/signup" v-if="!isAuthenticated" text>
        Зарегистрироваться
      </v-btn>
      <v-btn
        class="d-none d-sm-flex"
        text
        v-if="isAuthenticated"
        @click="logOut"
      >
        Выйти
      </v-btn>
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
