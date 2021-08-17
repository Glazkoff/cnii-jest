<template>
  <div class="text-center">
    <v-dialog v-model="innerDialog" width="500">
      <v-card>
        <v-card-text class="pt-4">
          <div class="text-center pb-2">
            <v-icon x-large color="success"> mdi-check-circle-outline </v-icon>
          </div>
          <div class="text-center mt-2">
            <h2>Вы успешно отправили заявку!</h2>
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
  name: "SendingConfirmationDialog",
  data() {
    return {
      innerDialog: this.$store.state.successRequestDialog
    };
  },
  watch: {
    "$store.state.successRequestDialog"() {
      this.innerDialog = this.$store.state.successRequestDialog;
    }
  }
};
</script>

<style lang="scss" scoped></style>
