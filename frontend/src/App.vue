<template>
  <router-view />
</template>

<script>
export default {
  name: "App",
  async mounted() {
    let refreshToken = localStorage.getItem("t");
    if (refreshToken !== null) {
      this.$store.commit("START_APP_LOADING");
      this.$store.dispatch("REFRESH_TOKEN").then(
        () => {
          this.$store.commit("STOP_APP_LOADING");
          let futurePath = "/";
          if (this.$store.state.first_path != null) {
            futurePath = this.$store.state.first_path;
          }
          if (
            this.$route.path != futurePath &&
            this.$route.path.substring(0, this.$route.path.length - 1) !=
              futurePath
          ) {
            this.$router.push({ path: futurePath });
          }
        },
        error => {
          this.$store.commit("STOP_APP_LOADING");
          if (error.code != "token_not_valid") console.log("ERROR: ", error);
        }
      );
    }
  },
  data: () => ({
    //
  })
};
</script>

<style lang="scss"></style>
