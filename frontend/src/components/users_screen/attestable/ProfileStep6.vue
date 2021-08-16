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
      <v-file-input
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
import { required } from "vuelidate/lib/validators";
import {
  SET_SIXTH_PROFILE_PART,
  UPDATE_REQUEST_STATUS
} from "@/graphql/user_request_mutations.js";
import { GET_SIXTH_PROFILE_PART } from "@/graphql/user_request_queries.js";
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
      form: {
        attestation_certificate_number: null,
        attestation_certificate_date: null,
        attestation_certificate_scan: null
      }
    };
  },
  apollo: {
    user: {
      query: GET_SIXTH_PROFILE_PART,
      variables() {
        return {
          userId: this.$store.getters.user_id
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
      if (val.attestationCertificateScan) {
        this.circleLoading1 = true;
        this.$http({
          url: "/media/" + val.attestationCertificateScan,
          method: "GET",
          responseType: "blob"
        }).then(response => {
          this.$v.form.$model.attestation_certificate_scan = new File(
            [response.data],
            val.attestationCertificateScan.split("/")[
              val.attestationCertificateScan.split("/").length - 1
            ]
          );
          this.circleLoading1 = false;
          this.$v.form.attestation_certificate_scan.$touch();
        });
      }
    }
  },
  validations: {
    form: {
      attestation_certificate_number: { required },
      attestation_certificate_date: { required },
      attestation_certificate_scan: { required }
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
        errors.push("Поле 'Скан сертификата аттестации' обязательно!");
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
      return new Promise((resolve, reject) => {
        this.$apollo
          .mutate({
            mutation: SET_SIXTH_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              attestationCertificateNumber:
                this.$v.form.$model.attestation_certificate_number,
              attestationCertificateDate:
                this.$v.form.$model.attestation_certificate_date,
              attestationCertificateScan:
                this.$v.form.$model.attestation_certificate_scan
            },
            update: (cache, { data: { setSixthProfilePart } }) => {
              const data = cache.readQuery({
                query: GET_SIXTH_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id
                }
              });

              data.user.attestationCertificateNumber =
                setSixthProfilePart.user.attestationCertificateNumber;
              data.user.attestationCertificateDate =
                setSixthProfilePart.user.attestationCertificateDate;
              data.user.attestationCertificateScan =
                setSixthProfilePart.user.attestationCertificateScan;

              cache.writeQuery({
                query: GET_SIXTH_PROFILE_PART,
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
