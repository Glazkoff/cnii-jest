<template>
  <div>
    <h1>Данные для аттестации</h1>
    <v-stepper v-model="stepperStatus" vertical>
      <v-stepper-step step="1" :complete="stepperStatus >= 1">
        Шаг 1. Личные данные
      </v-stepper-step>

      <v-stepper-content step="1">
        <ProfileStep1></ProfileStep1>
      </v-stepper-content>

      <v-stepper-step step="2" :complete="stepperStatus >= 2">
        Шаг 2
      </v-stepper-step>

      <v-stepper-content step="2">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="stepperStatus = 3"> Далее </v-btn>
        <v-btn text @click="stepperStatus = 1"> Назад </v-btn>
      </v-stepper-content>

      <v-stepper-step step="3"> Шаг 3 </v-stepper-step>

      <v-stepper-content step="3" :complete="stepperStatus >= 3">
        <v-card color="grey lighten-1" class="mb-12" height="200px"></v-card>
        <v-btn color="primary" @click="stepperStatus = 1"> Далее </v-btn>
        <v-btn text @click="stepperStatus = 2"> Назад </v-btn>
      </v-stepper-content>
    </v-stepper>
  </div>
</template>

<script>
import ProfileStep1 from "./ProfileStep1";

export default {
  name: "AttestableView",
  components: {
    ProfileStep1
  },
  data() {
    return {
      stepperStatus: 1
    };
  }
};
</script>

<style lang="scss" scoped></style>
