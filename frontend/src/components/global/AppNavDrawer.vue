<template>
  <v-list dense nav>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="text-h6">
          ЦНИИ Русского жестового языка
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-divider></v-divider>
    <v-list-item link v-if="isAuthenticated" to="/">
      <v-list-item-content>
        <v-list-item-title>Список заявок</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item link v-if="isAuthenticated" @click="logOut">
      <v-list-item-content>
        <v-list-item-title>Выйти</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item link v-if="!isAuthenticated" to="/login">
      <v-list-item-content>
        <v-list-item-title>Войти</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item link v-if="!isAuthenticated" to="/signup">
      <v-list-item-content>
        <v-list-item-title>Зарегистрироваться</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: "AppNavDrawer",
  methods: {
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
