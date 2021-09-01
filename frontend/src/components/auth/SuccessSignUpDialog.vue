<template>
  <div class="text-center">
    <v-dialog v-model="innerDialog" width="500">
      <v-card>
        <v-card-text class="pt-4">
          <div class="text-center pb-2">
            <v-icon x-large color="success"> mdi-check-circle-outline </v-icon>
          </div>
          <div class="text-center mt-2">
            <h2 class="mb-2">Вы успешно зарегистрировались!</h2>
            <p>
              На вашу электронную почту отправлено письмо перейдите по ссылке,
              чтобы подтвердить регистрацию
            </p>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="$emit('close')"> Закрыть </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "SuccessSignUpDialog",
  data() {
    return {
      innerDialog: this.$store.state.successSignUpDialog
    };
  },
  watch: {
    "$store.state.successSignUpDialog"() {
      this.innerDialog = this.$store.state.successSignUpDialog;
    }
  }
};
</script>

<style lang="scss" scoped></style>
