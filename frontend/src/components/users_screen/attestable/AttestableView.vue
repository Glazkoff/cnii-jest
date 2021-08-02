<template>
  <div>
    <h1 class="mb-2">Данные для аттестации</h1>
    <v-stepper v-model="stepperStatus" vertical>
      <v-stepper-step step="1" :complete="stepperStatus >= 1">
        Шаг 1. Личные данные
      </v-stepper-step>
      <v-stepper-content step="1">
        <ProfileStep1 @goToNextStep="stepperStatus = 2"></ProfileStep1>
      </v-stepper-content>

      <v-stepper-step step="2" :complete="stepperStatus >= 2">
        Шаг 2. Общая информация
      </v-stepper-step>
      <v-stepper-content step="2">
        <ProfileStep2
          @goToPrevStep="stepperStatus = 1"
          @goToNextStep="stepperStatus = 3"
        ></ProfileStep2>
      </v-stepper-content>

      <v-stepper-step step="3" :complete="stepperStatus >= 3">
        Шаг 3. Паспортные данные
      </v-stepper-step>
      <v-stepper-content step="3">
        <ProfileStep3
          @goToPrevStep="stepperStatus = 2"
          @goToNextStep="stepperStatus = 4"
        ></ProfileStep3>
      </v-stepper-content>

      <v-stepper-step step="4" :complete="stepperStatus >= 4">
        Шаг 4. Контактные данные
      </v-stepper-step>
      <v-stepper-content step="4">
        <ProfileStep4
          @goToPrevStep="stepperStatus = 3"
          @goToNextStep="stepperStatus = 5"
        ></ProfileStep4>
      </v-stepper-content>

      <v-stepper-step step="5" :complete="stepperStatus >= 5">
        Шаг 5. Опыт работы и награды
      </v-stepper-step>
      <v-stepper-content step="5">
        <ProfileStep5
          @goToPrevStep="stepperStatus = 4"
          @goToNextStep="confirmationDialog = true"
        ></ProfileStep5>
      </v-stepper-content>
    </v-stepper>
    <SendingConfirmationDialog
      :dialog="confirmationDialog"
      @close="confirmationDialog = false"
    ></SendingConfirmationDialog>
  </div>
</template>

<script>
import ProfileStep1 from "./ProfileStep1";
import ProfileStep2 from "./ProfileStep2";
import ProfileStep3 from "./ProfileStep3";
import ProfileStep4 from "./ProfileStep4";
import ProfileStep5 from "./ProfileStep5";
import SendingConfirmationDialog from "./SendingConfirmationDialog";

export default {
  name: "AttestableView",
  components: {
    ProfileStep1,
    ProfileStep2,
    ProfileStep3,
    ProfileStep4,
    ProfileStep5,
    SendingConfirmationDialog
  },
  data() {
    return {
      stepperStatus: 1,
      confirmationDialog: false
    };
  }
};
</script>

<style lang="scss" scoped></style>
