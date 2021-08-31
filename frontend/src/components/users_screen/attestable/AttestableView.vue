<template>
  <div>
    <h1 class="mb-2">Данные для аттестации</h1>
    <v-layout
      v-if="this.$apollo.queries.request.loading || stepperLoading"
      fill-height
    >
      <v-layout align-center d-flex fill-height justify-center wrap>
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-layout>
    </v-layout>
    <v-stepper v-model="stepperStatus" vertical v-else>
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
          @goToNextStep="stepperStatus = 6"
        ></ProfileStep5>
      </v-stepper-content>

      <v-stepper-step step="6" :complete="stepperStatus >= 6">
        Шаг 6. Теоретическая часть аттестации
      </v-stepper-step>
      <v-stepper-content step="6">
        <ProfileStep6
          @goToPrevStep="stepperStatus = 5"
          @goToNextStep="finishEditing()"
        ></ProfileStep6>
      </v-stepper-content>
    </v-stepper>
  </div>
</template>

<script>
import ProfileStep1 from "./ProfileStep1";
import ProfileStep2 from "./ProfileStep2";
import ProfileStep3 from "./ProfileStep3";
import ProfileStep4 from "./ProfileStep4";
import ProfileStep5 from "./ProfileStep5";
import ProfileStep6 from "./ProfileStep6";
import {
  REQUEST_STATUS,
  USER_REQUESTS
} from "@/graphql/user_request_queries.js";
import { FINISH_REQUEST } from "@/graphql/user_request_mutations.js";
export default {
  name: "AttestableView",
  components: {
    ProfileStep1,
    ProfileStep2,
    ProfileStep3,
    ProfileStep4,
    ProfileStep5,
    ProfileStep6
  },
  data() {
    return {
      stepperStatus: 1,
      stepperLoading: false
    };
  },
  apollo: {
    request: {
      query: REQUEST_STATUS,
      variables() {
        return {
          requestId: this.$route.params.id
        };
      }
    }
  },
  watch: {
    request(val) {
      if (val.status) {
        switch (val.status.toUpperCase()) {
          case "STEP_1":
            this.stepperStatus = 1;
            break;
          case "STEP_2":
            this.stepperStatus = 2;
            break;
          case "STEP_3":
            this.stepperStatus = 3;
            break;
          case "STEP_4":
            this.stepperStatus = 4;
            break;
          case "STEP_5":
            this.stepperStatus = 5;
            break;
          case "STEP_6":
            this.stepperStatus = 6;
            break;
          default:
            break;
        }
      }
    }
  },
  methods: {
    finishEditing() {
      this.stepperLoading = true;
      this.$apollo
        .mutate({
          mutation: FINISH_REQUEST,
          variables: { requestId: this.$route.params.id },
          update: (cache, { data: { finishRequest } }) => {
            let data = cache.readQuery({
              query: USER_REQUESTS,
              variables: {
                userId: this.$store.getters.user_id
              }
            });

            let findIndex = data.userRequests.findIndex(el => {
              return +el.id == +finishRequest.request.id;
            });
            if (findIndex != -1) {
              data.userRequests[findIndex].status =
                finishRequest.request.status;
              data.userRequests[findIndex].requestNumber =
                finishRequest.register.requestNumber;
            }
            cache.writeQuery({
              query: USER_REQUESTS,
              variables: {
                userId: this.$store.getters.user_id
              },
              data
            });
          }
        })

        .then(() => {
          this.$store.commit("OPEN_SUCCESS_DIALOG");
          this.$router.push("/");
        })
        .catch(() => {
          this.$store.commit("OPEN_ERROR_DIALOG");
        })
        .finally(() => {
          this.stepperLoading = false;
        });
    }
  }
};
</script>

<style lang="scss" scoped></style>
