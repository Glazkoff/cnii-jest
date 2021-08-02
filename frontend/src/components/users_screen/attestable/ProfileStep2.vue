<template>
  <div>
    <v-progress-circular
      indeterminate
      color="primary"
      v-if="this.$apollo.queries.user.loading"
    >
    </v-progress-circular>
    <v-form ref="form" lazy-validation v-else>
      <v-text-field
        label="Родной язык"
        autocomplete="language"
        v-model="$v.form.native_language.$model"
        :error-messages="nativeLanguageErrors"
        @input="
          $v.form.native_language.$touch();
          sendForm();
        "
        @blur="
          $v.form.native_language.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Гражданство"
        autocomplete="citizenship"
        v-model="$v.form.citizenship.$model"
        :error-messages="citizenshipErrors"
        @input="
          $v.form.citizenship.$touch();
          sendForm();
        "
        @blur="
          $v.form.citizenship.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Семейное положение"
        autocomplete="martial_status"
        v-model="$v.form.martial_status.$model"
        :error-messages="martialStatusErrors"
        @input="
          $v.form.martial_status.$touch();
          sendForm();
        "
        @blur="
          $v.form.martial_status.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Организация"
        autocomplete="organization"
        v-model="$v.form.organization.$model"
        :error-messages="organizationErrors"
        @input="
          $v.form.organization.$touch();
          sendForm();
        "
        @blur="
          $v.form.organization.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Занимаемая должность"
        autocomplete="job_position"
        v-model="$v.form.job_position.$model"
        :error-messages="jobPositionErrors"
        @input="
          $v.form.job_position.$touch();
          sendForm();
        "
        @blur="
          $v.form.job_position.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Образование"
        autocomplete="education"
        v-model="$v.form.education.$model"
        :error-messages="educationErrors"
        @input="
          $v.form.education.$touch();
          sendForm();
        "
        @blur="
          $v.form.education.$touch();
          sendForm();
        "
        required
      ></v-text-field>
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
// - native_language Родной язык
// - citizenship Гражданство
// - martial_status Семейное положение
// - organization Организация
// - job_position Занимаемая должность
// - education Образование

import { required } from "vuelidate/lib/validators";
import { SET_SECOND_PROFILE_PART } from "@/graphql/user_request_mutations.js";
import { GET_SECOND_PROFILE_PART } from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep2",
  data() {
    return {
      formLoading: false,
      form: {
        native_language: null,
        citizenship: null,
        martial_status: null,
        organization: null,
        job_position: null,
        education: null
      }
    };
  },
  apollo: {
    user: {
      query: GET_SECOND_PROFILE_PART,
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
        if (val.nativeLanguage) {
          this.$v.form.$model.native_language = val.nativeLanguage;
        }
        if (val.citizenship) {
          this.$v.form.$model.citizenship = val.citizenship;
        }
        if (val.martialStatus) {
          this.$v.form.$model.martial_status = val.martialStatus;
        }
        if (val.organization) {
          this.$v.form.$model.organization = val.organization;
        }
        if (val.jobPosition) {
          this.$v.form.$model.job_position = val.jobPosition;
        }
        if (val.education) {
          this.$v.form.$model.education = val.education;
        }
      }
    }
  },
  validations: {
    form: {
      native_language: { required },
      citizenship: { required },
      martial_status: { required },
      organization: { required },
      job_position: { required },
      education: { required }
    }
  },
  computed: {
    // TODO: add computed errors
    nativeLanguageErrors() {
      const errors = [];
      if (!this.$v.form.native_language.$dirty) return errors;
      !this.$v.form.native_language.required &&
        errors.push("Поле 'Родной язык' обязательно!");
      return errors;
    },
    citizenshipErrors() {
      const errors = [];
      if (!this.$v.form.citizenship.$dirty) return errors;
      !this.$v.form.citizenship.required &&
        errors.push("Поле 'Гражданство' обязательно!");
      return errors;
    },
    martialStatusErrors() {
      const errors = [];
      if (!this.$v.form.martial_status.$dirty) return errors;
      !this.$v.form.martial_status.required &&
        errors.push("Поле 'Семейное положение' обязательно!");
      return errors;
    },
    organizationErrors() {
      const errors = [];
      if (!this.$v.form.organization.$dirty) return errors;
      !this.$v.form.organization.required &&
        errors.push("Поле 'Организация' обязательно!");
      return errors;
    },
    jobPositionErrors() {
      const errors = [];
      if (!this.$v.form.job_position.$dirty) return errors;
      !this.$v.form.job_position.required &&
        errors.push("Поле 'Занимаемая должность' обязательно!");
      return errors;
    },
    educationErrors() {
      const errors = [];
      if (!this.$v.form.education.$dirty) return errors;
      !this.$v.form.education.required &&
        errors.push("Поле 'Образование' обязательно!");
      return errors;
    }
  },
  methods: {
    goToNextStep() {
      this.$v.form.$touch();
      if (!this.$v.form.$anyError) {
        this.formLoading = true;
        this.sendForm()
          .then(() => {
            this.$emit("goToNextStep");
          })
          .finally(() => {
            this.formLoading = false;
          });
      }
    },
    goToPrevStep() {
      this.formLoading = true;
      this.sendForm()
        .then(() => {
          this.$emit("goToPrevStep");
        })
        .finally(() => {
          this.formLoading = false;
        });
    },
    sendForm() {
      return new Promise((resolve, reject) => {
        this.$apollo
          .mutate({
            mutation: SET_SECOND_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              nativeLanguage: this.$v.form.$model.native_language,
              citizenship: this.$v.form.$model.citizenship,
              martialStatus: this.$v.form.$model.martial_status,
              organization: this.$v.form.$model.organization,
              jobPosition: this.$v.form.$model.job_position,
              education: this.$v.form.$model.education
            },
            update: (cache, { data: { setSecondProfilePart } }) => {
              const data = cache.readQuery({
                query: GET_SECOND_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id
                }
              });

              data.user.nativeLanguage =
                setSecondProfilePart.user.nativeLanguage;
              data.user.citizenship = setSecondProfilePart.user.citizenship;
              data.user.martialStatus = setSecondProfilePart.user.martialStatus;
              data.user.organization = setSecondProfilePart.user.organization;
              data.user.jobPosition = setSecondProfilePart.user.jobPosition;
              data.user.education = setSecondProfilePart.user.education;

              cache.writeQuery({
                query: GET_SECOND_PROFILE_PART,
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
