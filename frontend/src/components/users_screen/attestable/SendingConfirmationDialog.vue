<template>
  <div class="text-center">
    <v-dialog v-model="innerDialog" width="500">
      <v-card>
        <v-card-text>
          <div>
            <v-icon large color="primary"> mdi-email-send </v-icon>
          </div>
          <div>Вы уверены, что хотите отправить заявку?</div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="$emit('close')"> I accept </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "SendingConfirmationDialog",
  props: ["dialog"],
  data() {
    return {
      innerDialog: false
    };
  },
  watch: {
    dialog(val) {
      this.innerDialog = val;
      if (val == false) {
        this.$emit("close");
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
