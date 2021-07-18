<template>
  <v-container fill-height>
    <v-layout align-center="align-center" justify-center="justify-center">
      <router-view></router-view>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: "Auth"
};
</script>

<style lang="scss" scoped>
.auth-form {
  max-width: 500px;
}
.v-main {
  max-height: calc(100vh - 56px);
}
</style>
