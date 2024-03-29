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
        label="Номер сертификата аттестации"
        v-model="$v.form.attestation_certificate_number.$model"
        :error-messages="attestationCertificateNumberErrors"
        @input="
          $v.form.attestation_certificate_number.$touch();
          sendForm();
        "
        @blur="
          $v.form.attestation_certificate_number.$touch();
          sendForm();
        "
        :disabled="formLoading"
        required
      ></v-text-field>
      <DatePicker
        label="Дата выдачи сертификата аттестации"
        @update="
          $v.form.attestation_certificate_date.$model = $event;
          sendForm();
        "
        :disabled="formLoading"
        :errors="attestationСertificateDateErrors"
        :max="new Date().toISOString().slice(0, 10)"
        :predefined="predefinedAttestationСertificateDate"
      ></DatePicker>
      <div
        class="mb-4"
        v-if="
          user.attestationCertificateScan && !uploadAttestationCertificateScan
        "
      >
        <small>Скан сертификата аттестации</small><br />
        <v-btn
          color="success"
          text
          block
          small
          @click="
            uploadAttestationCertificateScan = true;
            user.attestationCertificateScan = null;
            $v.form.attestation_certificate_scan.$model = null;
          "
        >
          Выбрать другой файл
        </v-btn>
        <v-img
          :src="`/media/${user.attestationCertificateScan}`"
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
        label="Скан сертификата аттестации"
        prepend-icon="mdi-camera"
        :error-messages="attestationСertificateScanErrors"
        v-model="$v.form.attestation_certificate_scan.$model"
        @input="sendForm()"
        @blur="sendForm()"
      ></v-file-input>
      <div
        class="mb-4"
        v-if="(request != undefined ? request.cheque : false) && !uploadCheque"
      >
        <small>Чек об оплате организационного взноса</small><br />
        <v-btn
          color="success"
          text
          block
          small
          @click="
            uploadCheque = true;
            request.cheque = null;
            $v.form.cheque.$model = null;
          "
        >
          Выбрать другой файл
        </v-btn>
        <v-img
          :src="`/media/${request.cheque}`"
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
        label="Чек об оплате орг. взноса"
        prepend-icon="mdi-camera"
        :error-messages="chequeErrors"
        v-model="$v.form.cheque.$model"
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
import { required, requiredIf } from "vuelidate/lib/validators";
import {
  SET_SIXTH_PROFILE_PART,
  UPDATE_REQUEST_STATUS
} from "@/graphql/user_request_mutations.js";
import {
  GET_SIXTH_PROFILE_PART,
  USER_REQUESTS,
  REQUEST_CHEQUE
} from "@/graphql/user_request_queries.js";
import DatePicker from "../../global/DatePicker.vue";

export default {
  name: "ProfileStep6",
  components: {
    DatePicker
  },
  data() {
    return {
      formLoading: false,
      circleLoading1: false,
      circleLoading2: false,
      uploadAttestationCertificateScan: false,
      uploadCheque: false,
      form: {
        attestation_certificate_number: null,
        attestation_certificate_date: null,
        attestation_certificate_scan: null,
        cheque: null
      }
    };
  },
  apollo: {
    user: {
      query: GET_SIXTH_PROFILE_PART,
      variables() {
        return {
          userId: this.$store.getters.user_id,
          requestId: this.$route.params.id
        };
      }
    },
    request: {
      query: REQUEST_CHEQUE,
      variables() {
        return {
          requestId: this.$route.params.id
        };
      }
    }
  },
  watch: {
    user: function (val) {
      if (val.attestationCertificateNumber) {
        this.$v.form.$model.attestation_certificate_number =
          val.attestationCertificateNumber;
      }
      if (val.attestationCertificateDate) {
        this.$v.form.$model.attestation_certificate_date =
          val.attestationCertificateDate;
      }
    }
  },
  validations: {
    form: {
      attestation_certificate_number: { required },
      attestation_certificate_date: { required },
      attestation_certificate_scan: {
        required: requiredIf(function () {
          return (
            !this.user.attestationCertificateScan ||
            this.uploadAttestationCertificateScan
          );
        })
      },
      cheque: {
        required: requiredIf(function () {
          return !this.request.cheque || this.uploadCheque;
        })
      }
    }
  },
  computed: {
    attestationCertificateNumberErrors() {
      const errors = [];
      if (!this.$v.form.attestation_certificate_number.$dirty) return errors;
      !this.$v.form.attestation_certificate_number.required &&
        errors.push("Поле 'Номер сертификата аттестации' обязательно!");
      return errors;
    },
    attestationСertificateDateErrors() {
      const errors = [];
      if (!this.$v.form.attestation_certificate_date.$dirty) return errors;
      !this.$v.form.attestation_certificate_date.required &&
        errors.push("Поле 'Дата выдачи сертификата аттестации' обязательно!");
      return errors;
    },
    attestationСertificateScanErrors() {
      const errors = [];
      if (!this.$v.form.attestation_certificate_scan.$dirty) return errors;
      !this.$v.form.attestation_certificate_scan.required &&
        (this.form.attestationCertificateScan == null ||
          this.form.attestationCertificateScan == "" ||
          !this.uploadAttestationCertificateScan) &&
        errors.push("Поле 'Скан сертификата аттестации' обязательно!");
      return errors;
    },
    chequeErrors() {
      const errors = [];
      if (!this.$v.form.cheque.$dirty) return errors;
      !this.$v.form.cheque.required &&
        (this.form.cheque == null ||
          this.form.cheque == "" ||
          !this.uploadCheque) &&
        errors.push("Поле 'Чек об оплате орг. взноса' обязательно!");
      return errors;
    },
    predefinedAttestationСertificateDate() {
      if (this.user) {
        if (this.user.attestationCertificateDate) {
          return this.user.attestationCertificateDate;
        } else {
          return null;
        }
      } else {
        return null;
      }
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
          this.sendCurrentStep(5).finally(() => {
            this.$emit("goToPrevStep");
            this.formLoading = false;
          });
        })
        .catch(() => {
          this.formLoading = false;
        });
    },
    sendForm() {
      if (this.$v.form.$model.attestation_certificate_scan) {
        this.uploadAttestationCertificateScan = false;
      }
      if (this.$v.form.$model.cheque) {
        this.uploadCheque = false;
      }
      return new Promise((resolve, reject) => {
        this.$apollo
          .mutate({
            mutation: SET_SIXTH_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              requestId: this.$route.params.id,
              attestationCertificateNumber:
                this.$v.form.$model.attestation_certificate_number,
              attestationCertificateDate:
                this.$v.form.$model.attestation_certificate_date,
              attestationCertificateScan:
                this.$v.form.$model.attestation_certificate_scan,
              cheque: this.$v.form.$model.cheque
            },
            update: (cache, { data: { setSixthProfilePart } }) => {
              const data = cache.readQuery({
                query: GET_SIXTH_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id,
                  requestId: this.$route.params.id
                }
              });

              data.user.attestationCertificateNumber =
                setSixthProfilePart.user.attestationCertificateNumber;
              data.user.attestationCertificateDate =
                setSixthProfilePart.user.attestationCertificateDate;
              data.user.attestationCertificateScan =
                setSixthProfilePart.user.attestationCertificateScan;
              data.request.cheque = setSixthProfilePart.request.cheque;

              cache.writeQuery({
                query: GET_SIXTH_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id,
                  requestId: this.$route.params.id
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
