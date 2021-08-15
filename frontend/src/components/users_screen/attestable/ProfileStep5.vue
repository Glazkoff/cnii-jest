<template>
  <div>
    <div
      v-if="
        this.$apollo.queries.user.loading || circleLoading || circleLoading2
      "
    >
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
    <v-form ref="form" lazy-validation v-else>
      <v-text-field
        label="Стаж полных лет"
        v-model="$v.form.work_experience_full_years.$model"
        :error-messages="workExperienceFullYearsErrors"
        @input="
          $v.form.work_experience_full_years.$touch();
          sendForm();
        "
        @blur="
          $v.form.work_experience_full_years.$touch();
          sendForm();
        "
        type="number"
        required
      ></v-text-field>
      <v-text-field
        label="Стаж настоящей должности"
        v-model="$v.form.work_experience_current_job.$model"
        :error-messages="workExperienceCurrentJobErrors"
        @input="
          $v.form.work_experience_current_job.$touch();
          sendForm();
        "
        @blur="
          $v.form.work_experience_current_job.$touch();
          sendForm();
        "
        type="number"
        required
      ></v-text-field>
      <v-textarea
        label="Наличие наград"
        v-model="$v.form.awards.$model"
        :error-messages="awardsErrors"
        @input="
          $v.form.awards.$touch();
          sendForm();
        "
        @blur="
          $v.form.awards.$touch();
          sendForm();
        "
        hint="Опишите ваш список наград"
        auto-grow
        rows="2"
        class="mb-2"
        required
      ></v-textarea>
      <v-textarea
        label="Повышение квалификации"
        v-model="$v.form.training.$model"
        :error-messages="trainingErrors"
        @input="
          $v.form.training.$touch();
          sendForm();
        "
        @blur="
          $v.form.training.$touch();
          sendForm();
        "
        hint="Опишите ваше повышение квалификации"
        auto-grow
        rows="2"
        class="mb-2"
        required
      ></v-textarea>
      <v-textarea
        label="Членство в организациях"
        v-model="$v.form.organization_membership.$model"
        :error-messages="organizationMembershipErrors"
        @input="
          $v.form.organization_membership.$touch();
          sendForm();
        "
        @blur="
          $v.form.organization_membership.$touch();
          sendForm();
        "
        hint="Опишите ваше членство в организациях"
        auto-grow
        rows="2"
        class="mb-2"
        required
      ></v-textarea>
      <v-file-input
        chips
        accept="image/png, image/jpeg, image/bmp"
        placeholder="Прикрепите скан"
        label="Характеристика"
        prepend-icon="mdi-camera"
        :error-messages="characteristicErrors"
        v-model="$v.form.characteristic.$model"
        @input="sendForm()"
        @blur="sendForm()"
      ></v-file-input>
      <v-file-input
        chips
        accept="application/pdf"
        placeholder="Прикрепите скан"
        label="Заверенная копия трудовой книжки (все страницы)"
        prepend-icon="mdi-file-document-outline"
        :error-messages="employmentHistoryErrors"
        v-model="$v.form.employment_history.$model"
      ></v-file-input>
    </v-form>
    <v-btn
      class="mt-2"
      color="primary"
      :disabled="$v.form.$anyError"
      @click="goToNextStep"
      v-if="!this.$apollo.queries.user.loading"
    >
      Отправить
    </v-btn>
    <v-btn
      text
      class="mt-2"
      :disabled="$v.form.$anyError"
      @click="goToPrevStep"
      v-if="!this.$apollo.queries.user.loading"
    >
      Назад
    </v-btn>
  </div>
</template>

<script>
// TODO:
// - work_experience_full_years Стаж полных лет
// - work_experience_current_job Стаж настоящей должности
// - awards Наличие наград
// - training Повышение квалификации
// - organization_membership Членство в организациях

import { required } from "vuelidate/lib/validators";
import {
  SET_FIFTH_PROFILE_PART,
  UPDATE_REQUEST_STATUS
} from "@/graphql/user_request_mutations.js";
import { GET_FIFTH_PROFILE_PART } from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep5",
  data() {
    return {
      formLoading: false,
      circleLoading: false,
      circleLoading2: false,
      form: {
        work_experience_full_years: null,
        work_experience_current_job: null,
        awards: null,
        training: null,
        organization_membership: null
      }
    };
  },
  apollo: {
    user: {
      query: GET_FIFTH_PROFILE_PART,
      variables() {
        return {
          userId: this.$store.getters.user_id
        };
      }
    }
  },
  watch: {
    user: function (val) {
      if (val) {
        if (val.workExperienceFullYears) {
          this.$v.form.$model.work_experience_full_years =
            val.workExperienceFullYears;
        }
        if (val.workExperienceCurrentJob) {
          this.$v.form.$model.work_experience_current_job =
            val.workExperienceCurrentJob;
        }
        if (val.awards) {
          this.$v.form.$model.awards = val.awards;
        }
        if (val.training) {
          this.$v.form.$model.training = val.training;
        }
        if (val.organizationMembership) {
          this.$v.form.$model.organization_membership =
            val.organizationMembership;
        }
        if (val.characteristic) {
          this.circleLoading = true;
          this.$http({
            url: "/media/" + val.characteristic,
            method: "GET",
            responseType: "blob"
          }).then(response => {
            this.$v.form.$model.characteristic = new File(
              [response.data],
              val.characteristic.split("/")[
                val.characteristic.split("/").length - 1
              ]
            );
            this.circleLoading = false;
            this.$v.form.characteristic.$touch();
          });
        }
        if (val.employmentHistory) {
          this.circleLoading2 = true;
          this.$http({
            url: "/media/" + val.employmentHistory,
            method: "GET",
            responseType: "blob"
          }).then(response => {
            this.$v.form.$model.employment_history = new File(
              [response.data],
              val.employmentHistory.split("/")[
                val.employmentHistory.split("/").length - 1
              ]
            );
            this.circleLoading2 = false;
            this.$v.form.employment_history.$touch();
          });
        }
      }
    }
  },
  validations: {
    form: {
      work_experience_full_years: { required },
      work_experience_current_job: { required },
      awards: { required },
      training: { required },
      organization_membership: { required },
      characteristic: { required },
      employment_history: { required }
    }
  },
  computed: {
    workExperienceFullYearsErrors() {
      const errors = [];
      if (!this.$v.form.work_experience_full_years.$dirty) return errors;
      !this.$v.form.work_experience_full_years.required &&
        errors.push("Поле 'Стаж полных лет' обязательно!");
      return errors;
    },
    workExperienceCurrentJobErrors() {
      const errors = [];
      if (!this.$v.form.work_experience_current_job.$dirty) return errors;
      !this.$v.form.work_experience_current_job.required &&
        errors.push("Поле 'Стаж настоящей должности' обязательно!");
      return errors;
    },
    awardsErrors() {
      const errors = [];
      if (!this.$v.form.awards.$dirty) return errors;
      !this.$v.form.awards.required &&
        errors.push("Поле 'Наличие наград' обязательно!");
      return errors;
    },
    trainingErrors() {
      const errors = [];
      if (!this.$v.form.training.$dirty) return errors;
      !this.$v.form.training.required &&
        errors.push("Поле 'Повышение квалификации' обязательно!");
      return errors;
    },
    organizationMembershipErrors() {
      const errors = [];
      if (!this.$v.form.organization_membership.$dirty) return errors;
      !this.$v.form.organization_membership.required &&
        errors.push("Поле 'Членство в организациях' обязательно!");
      return errors;
    },
    characteristicErrors() {
      const errors = [];
      if (!this.$v.form.characteristic.$dirty) return errors;
      !this.$v.form.characteristic.required &&
        errors.push("Поле 'Характеристика' обязательно!");
      return errors;
    },
    employmentHistoryErrors() {
      const errors = [];
      if (!this.$v.form.employment_history.$dirty) return errors;
      !this.$v.form.employment_history.required &&
        errors.push("Поле 'Копия трудовой книжки' обязательно!");
      return errors;
    }
  },
  methods: {
    sendCurrentStep(stepNumber) {
      return new Promise((resolve, reject) => {
        this.$apollo
          .mutate({
            mutation: UPDATE_REQUEST_STATUS,
            variables: {
              requestId: this.$route.params.id,
              statusNumber: stepNumber
            }
          })
          .then(() => {
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },
    goToNextStep() {
      this.$v.form.$touch();
      if (!this.$v.form.$anyError) {
        this.formLoading = true;
        this.sendForm()
          .then(() => {
            this.$emit("goToNextStep");
            this.formLoading = false;
          })
          .catch(() => {
            this.formLoading = false;
          });
      }
    },
    goToPrevStep() {
      this.formLoading = true;
      this.sendForm()
        .then(() => {
          this.sendCurrentStep(4).finally(() => {
            this.$emit("goToPrevStep");
            this.formLoading = false;
          });
        })
        .catch(() => {
          this.formLoading = false;
        });
    },
    sendForm() {
      console.log(this.$v.form.$model.characteristic);
      return new Promise((resolve, reject) => {
        this.$apollo
          .mutate({
            mutation: SET_FIFTH_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              workExperienceFullYears:
                this.$v.form.$model.work_experience_full_years,
              workExperienceCurrentJob:
                this.$v.form.$model.work_experience_current_job,
              awards: this.$v.form.$model.awards,
              training: this.$v.form.$model.training,
              organizationMembership:
                this.$v.form.$model.organization_membership,
              characteristic: this.$v.form.$model.characteristic,
              employmentHistory: this.$v.form.$model.employment_history
            },
            update: (cache, { data: { setFifthProfilePart } }) => {
              const data = cache.readQuery({
                query: GET_FIFTH_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id
                }
              });

              data.user.workExperienceFullYears =
                setFifthProfilePart.user.workExperienceFullYears;
              data.user.workExperienceCurrentJob =
                setFifthProfilePart.user.workExperienceCurrentJob;
              data.user.awards = setFifthProfilePart.user.awards;
              data.user.training = setFifthProfilePart.user.training;
              data.user.organizationMembership =
                setFifthProfilePart.user.organizationMembership;

              cache.writeQuery({
                query: GET_FIFTH_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id
                },
                data
              });
            }
          })
          .then(res => {
            resolve(res);
          })
          .catch(err => {
            reject(err);
          });
      });
    }
  }
};
</script>

<style lang="scss" scoped></style>
