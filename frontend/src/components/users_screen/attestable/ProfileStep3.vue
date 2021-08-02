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
        label="Данные паспорта"
        autocomplete="passport"
        v-model="$v.form.passport.$model"
        :error-messages="passportErrors"
        @input="
          $v.form.passport.$touch();
          sendForm();
        "
        @blur="
          $v.form.passport.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-file-input
        chips
        accept="image/png, image/jpeg, image/bmp"
        placeholder="Прикрепите скан"
        label="Скан паспорта - страницы 2-3 (разворот с фотографией)"
        prepend-icon="mdi-camera"
        :error-messages="passportPart1ScanErrors"
        v-model="$v.form.passport_part1_scan.$model"
        @input="sendForm()"
        @blur="sendForm()"
      ></v-file-input>
      <v-file-input
        chips
        accept="image/png, image/jpeg, image/bmp"
        placeholder="Прикрепите скан"
        label="Скан паспорта - страницы 4-5 (разворот с фотографией)"
        prepend-icon="mdi-camera"
        :error-messages="passportPart2ScanErrors"
        v-model="$v.form.passport_part2_scan.$model"
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
// - passport Данные паспорта
// - passport_part1_scan Скан паспорта (часть 1)
// - passport_part2_scan Скан паспорта (часть 2)

import { required } from "vuelidate/lib/validators";
import { SET_THIRD_PROFILE_PART } from "@/graphql/user_request_mutations.js";
import { GET_THIRD_PROFILE_PART } from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep3",
  data() {
    return {
      formLoading: false,
      form: {
        passport: null,
        passport_part1_scan: null,
        passport_part2_scan: null
      }
    };
  },
  apollo: {
    user: {
      query: GET_THIRD_PROFILE_PART,
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
        if (val.passport) {
          this.$v.form.$model.passport = val.passport;
        }
        if (val.passportPart1Scan) {
          this.$http({
            url: "/media/" + val.passportPart1Scan,
            method: "GET",
            responseType: "blob"
          }).then(response => {
            this.$v.form.$model.passport_part1_scan = new File(
              [response.data],
              val.passportPart1Scan.split("/")[
                val.passportPart1Scan.split("/").length - 1
              ]
            );
          });
        }
        if (val.passportPart2Scan) {
          this.$http({
            url: "/media/" + val.passportPart1Scan,
            method: "GET",
            responseType: "blob"
          }).then(response => {
            this.$v.form.$model.passport_part2_scan = new File(
              [response.data],
              val.passportPart2Scan.split("/")[
                val.passportPart2Scan.split("/").length - 1
              ]
            );
          });
        }
      }
    }
  },
  validations: {
    form: {
      passport: { required },
      passport_part1_scan: { required },
      passport_part2_scan: { required }
    }
  },
  computed: {
    passportErrors() {
      const errors = [];
      if (!this.$v.form.passport.$dirty) return errors;
      !this.$v.form.passport.required &&
        errors.push("Поле 'Данные паспорта' обязательно!");
      return errors;
    },
    passportPart1ScanErrors() {
      const errors = [];
      if (!this.$v.form.passport_part1_scan.$dirty) return errors;
      !this.$v.form.passport_part1_scan.required &&
        errors.push("Поле 'Скан паспорта (часть 1)' обязательно!");
      return errors;
    },
    passportPart2ScanErrors() {
      const errors = [];
      if (!this.$v.form.passport_part2_scan.$dirty) return errors;
      !this.$v.form.passport_part2_scan.required &&
        errors.push("Поле 'Скан паспорта (часть 2)' обязательно!");
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
            mutation: SET_THIRD_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              passport: this.$v.form.$model.passport,
              passportPart1Scan: this.$v.form.$model.passport_part1_scan,
              passportPart2Scan: this.$v.form.$model.passport_part2_scan
            },
            update: (cache, { data: { setThirdProfilePart } }) => {
              const data = cache.readQuery({
                query: GET_THIRD_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id
                }
              });

              data.user.passport = setThirdProfilePart.user.passport;

              cache.writeQuery({
                query: GET_THIRD_PROFILE_PART,
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
