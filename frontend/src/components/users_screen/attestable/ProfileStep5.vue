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
      <v-select
        :items="selectYears()"
        item-text="text"
        item-value="value"
        label="Год начала трудовой деятельности"
        v-model="$v.form.full_work_experience_start_year.$model"
        :error-messages="fullWorkExperienceStartYearErrors"
        @input="
          $v.form.full_work_experience_start_year.$touch();
          sendForm();
        "
        @blur="
          $v.form.full_work_experience_start_year.$touch();
          sendForm();
        "
      ></v-select>
      <v-select
        :items="selectYears()"
        item-text="text"
        item-value="value"
        label="Стаж настоящей должности"
        v-model="$v.form.current_job_experience_start_year.$model"
        :error-messages="currentJobExperienceStartYearErrors"
        @input="
          $v.form.current_job_experience_start_year.$touch();
          sendForm();
        "
        @blur="
          $v.form.current_job_experience_start_year.$touch();
          sendForm();
        "
      ></v-select>
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
      <div class="mb-4" v-if="user.characteristic && !uploadCharacteristic">
        <small>Характеристика</small><br />
        <v-btn
          color="success"
          text
          block
          small
          @click="
            uploadCharacteristic = true;
            user.characteristic = null;
            $v.form.characteristic.$model = null;
          "
        >
          Выбрать другой файл
        </v-btn>
        <v-img
          :src="`/media/${user.characteristic}`"
          aspect-ratio="1"
          max-height="200"
          contain
          class="grey lighten-2"
        >
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
              <v-progress-circular
                indeterminate
                color="grey lighten-5"
              ></v-progress-circular>
            </v-row>
          </template>
        </v-img>
      </div>
      <v-file-input
        v-else
        chips
        accept="image/png, image/jpeg, image/bmp"
        :messages="[
          'Загрузите в формате png, jpeg, jpg, pjp, pjpeg, jfif, bmp'
        ]"
        placeholder="Прикрепите скан"
        label="Характеристика"
        prepend-icon="mdi-camera"
        class="mb-2"
        :error-messages="characteristicErrors"
        v-model="$v.form.characteristic.$model"
        @input="sendForm()"
        @blur="sendForm()"
      ></v-file-input>
      <div
        class="mb-4"
        v-if="user.employmentHistory && !uploadEmploymentHistory"
      >
        <small>Заверенная копия трудовой книжки (все страницы)</small><br />
        <v-btn
          color="success"
          text
          block
          small
          @click="
            uploadEmploymentHistory = true;
            user.employmentHistory = null;
            $v.form.employment_history.$model = null;
          "
        >
          Выбрать другой файл
        </v-btn>
        <embed
          :src="`/media/${user.employmentHistory}`"
          aspect-ratio="1"
          height="200px"
          width="100%"
        />
      </div>
      <v-file-input
        v-else
        chips
        accept="application/pdf"
        placeholder="Прикрепите скан"
        label="Заверенная копия трудовой книжки (все страницы)"
        prepend-icon="mdi-file-document-outline"
        :error-messages="employmentHistoryErrors"
        v-model="$v.form.employment_history.$model"
        :messages="['Загрузите в формате pdf']"
        @input="sendForm()"
        @blur="sendForm()"
      ></v-file-input>
    </v-form>
    <v-btn
      class="mt-2"
      color="primary"
      :disabled="$v.form.$anyError"
      @click="goToNextStep"
      v-if="!this.$apollo.queries.user.loading"
    >
      Далее
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
// - full_work_experience_start_year Стаж полных лет
// - current_job_experience_start_year Стаж настоящей должности
// - awards Наличие наград
// - training Повышение квалификации
// - organization_membership Членство в организациях

import { required, requiredIf } from "vuelidate/lib/validators";
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
      uploadCharacteristic: false,
      uploadEmploymentHistory: false,
      form: {
        full_work_experience_start_year: null,
        current_job_experience_start_year: null,
        awards: null,
        training: null,
        organization_membership: null,
        characteristic: null,
        employment_history: null
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
        if (val.fullWorkExperienceStartYear) {
          this.$v.form.$model.full_work_experience_start_year =
            val.fullWorkExperienceStartYear.split("A_")[1];
        }
        if (val.currentJobExperienceStartYear) {
          this.$v.form.$model.current_job_experience_start_year =
            val.currentJobExperienceStartYear.split("A_")[1];
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
      }
    }
  },
  validations: {
    form: {
      full_work_experience_start_year: { required },
      current_job_experience_start_year: { required },
      awards: { required },
      training: { required },
      organization_membership: { required },
      characteristic: {
        required: requiredIf(function () {
          return !this.user.characteristic || this.uploadCharacteristic;
        })
      },
      employment_history: {
        required: requiredIf(function () {
          return !this.user.employmentHistory || this.uploadEmploymentHistory;
        })
      }
    }
  },
  computed: {
    fullWorkExperienceStartYearErrors() {
      const errors = [];
      if (!this.$v.form.full_work_experience_start_year.$dirty) return errors;
      !this.$v.form.full_work_experience_start_year.required &&
        errors.push("Поле 'Год начада трудовой деятельности' обязательно!");
      return errors;
    },
    currentJobExperienceStartYearErrors() {
      const errors = [];
      if (!this.$v.form.current_job_experience_start_year.$dirty) return errors;
      !this.$v.form.current_job_experience_start_year.required &&
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
        !(this.user.characteristic || !this.uploadCharacteristic) &&
        errors.push("Поле 'Характеристика' обязательно!");
      return errors;
    },
    employmentHistoryErrors() {
      const errors = [];
      if (!this.$v.form.employment_history.$dirty) return errors;
      !this.$v.form.employment_history.required &&
        !(this.user.employmentHistory || !this.uploadEmploymentHistory) &&
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
            this.sendCurrentStep(6).finally(() => {
              this.$emit("goToNextStep");
              this.formLoading = false;
            });
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
      if (this.$v.form.$model.characteristic) {
        this.uploadCharacteristic = false;
      }
      if (this.$v.form.$model.employment_history) {
        this.uploadEmploymentHistory = false;
      }
      return new Promise((resolve, reject) => {
        this.$apollo
          .mutate({
            mutation: SET_FIFTH_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              fullWorkExperienceStartYear:
                this.$v.form.$model.full_work_experience_start_year,
              currentJobExperienceStartYear:
                this.$v.form.$model.current_job_experience_start_year,
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

              data.user.fullWorkExperienceStartYear =
                setFifthProfilePart.user.fullWorkExperienceStartYear;
              data.user.currentJobExperienceStartYear =
                setFifthProfilePart.user.currentJobExperienceStartYear;
              data.user.awards = setFifthProfilePart.user.awards;
              data.user.training = setFifthProfilePart.user.training;
              data.user.organizationMembership =
                setFifthProfilePart.user.organizationMembership;
              data.user.characteristic =
                setFifthProfilePart.user.characteristic;
              data.user.employmentHistory =
                setFifthProfilePart.user.employmentHistory;

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
    },
    selectYears() {
      let yearArr = [];
      for (let year = new Date().getFullYear(); year >= 1950; year--) {
        yearArr.push({ text: "" + year, value: "" + year });
      }
      return yearArr;
    }
  }
};
</script>

<style lang="scss" scoped></style>
