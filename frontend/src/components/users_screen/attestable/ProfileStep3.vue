<template>
  <div>
    <div
      v-if="
        this.$apollo.queries.user.loading || circleLoading1 || circleLoading2
      "
    >
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>
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
      <div
        class="mb-4"
        v-if="user.passportPart1Scan && !uploadPassportPart1Scan"
      >
        <small>Скан паспорта - страницы 2-3 (разворот с фотографией)</small
        ><br />
        <v-btn
          color="success"
          text
          block
          small
          @click="
            uploadPassportPart1Scan = true;
            user.passportPart1Scan = null;
            $v.form.passport_part1_scan.$model = null;
          "
        >
          Выбрать другой файл
        </v-btn>
        <v-img
          :src="`/media/${user.passportPart1Scan}`"
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
        placeholder="Прикрепите скан"
        :messages="[
          'Загрузите в формате png, jpeg, jpg, pjp, pjpeg, jfif, bmp'
        ]"
        class="mb-2"
        label="Скан паспорта - страницы 2-3 (разворот с фотографией)"
        prepend-icon="mdi-camera"
        :error-messages="passportPart1ScanErrors"
        v-model="$v.form.passport_part1_scan.$model"
        @input="sendForm()"
        @blur="sendForm()"
      ></v-file-input>
      <div
        class="mb-4"
        v-if="user.passportPart2Scan && !uploadPassportPart2Scan"
      >
        <small>Скан паспорта - страницы 4-5 (разворот с фотографией)</small
        ><br />
        <v-btn
          color="success"
          text
          block
          small
          @click="
            uploadPassportPart2Scan = true;
            user.passportPart2Scan = null;
            $v.form.passport_part2_scan.$model = null;
          "
        >
          Выбрать другой файл
        </v-btn>
        <v-img
          :src="`/media/${user.passportPart2Scan}`"
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
        placeholder="Прикрепите скан"
        label="Скан паспорта - страницы 4-5 (разворот с фотографией)"
        prepend-icon="mdi-camera"
        :messages="[
          'Загрузите в формате png, jpeg, jpg, pjp, pjpeg, jfif, bmp'
        ]"
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
      v-if="
        !this.$apollo.queries.user.loading && !circleLoading1 && !circleLoading2
      "
    >
      Далее
    </v-btn>
    <v-btn
      text
      class="mt-2"
      :disabled="$v.form.$anyError"
      @click="goToPrevStep"
      v-if="
        !this.$apollo.queries.user.loading && !circleLoading1 && !circleLoading2
      "
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

import { required, requiredIf } from "vuelidate/lib/validators";
import {
  SET_THIRD_PROFILE_PART,
  UPDATE_REQUEST_STATUS
} from "@/graphql/user_request_mutations.js";
import {
  GET_THIRD_PROFILE_PART,
  USER_REQUESTS
} from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep3",
  data() {
    return {
      formLoading: false,
      circleLoading1: false,
      circleLoading2: false,
      uploadPassportPart1Scan: false,
      uploadPassportPart2Scan: false,
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
      }
    }
  },
  validations: {
    form: {
      passport: { required },
      passport_part1_scan: {
        required: requiredIf(function () {
          return !this.user.passportPart1Scan || this.uploadPassportPart1Scan;
        })
      },
      passport_part2_scan: {
        required: requiredIf(function () {
          return !this.user.passportPart2Scan || this.uploadPassportPart2Scan;
        })
      }
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
        !(this.user.passportPart1Scan || !this.uploadPassportPart1Scan) &&
        errors.push("Поле 'Скан паспорта (часть 1)' обязательно!");
      return errors;
    },
    passportPart2ScanErrors() {
      const errors = [];
      if (!this.$v.form.passport_part2_scan.$dirty) return errors;
      !this.$v.form.passport_part2_scan.required &&
        !(this.user.passportPart2Scan || !this.uploadPassportPart2Scan) &&
        errors.push("Поле 'Скан паспорта (часть 2)' обязательно!");
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
            },
            update: (cache, { data: { updateRequestStatus } }) => {
              let data = cache.readQuery({
                query: USER_REQUESTS,
                variables: {
                  userId: this.$store.getters.user_id
                }
              });
              let findIndex = data.userRequests.findIndex(el => {
                el.id == updateRequestStatus.request.id;
              });
              if (findIndex != -1) {
                data.userRequests[findIndex].status =
                  updateRequestStatus.request.status;
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
            this.sendCurrentStep(4).finally(() => {
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
          this.sendCurrentStep(2).finally(() => {
            this.$emit("goToPrevStep");
            this.formLoading = false;
          });
        })
        .catch(() => {
          this.formLoading = false;
        });
    },
    sendForm() {
      if (this.$v.form.$model.passport_part1_scan) {
        this.uploadPassportPart1Scan = false;
      }
      if (this.$v.form.$model.passport_part2_scan) {
        this.uploadPassportPart2Scan = false;
      }
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
              data.user.passportPart1Scan =
                setThirdProfilePart.user.passportPart1Scan;
              data.user.passportPart2Scan =
                setThirdProfilePart.user.passportPart2Scan;

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
