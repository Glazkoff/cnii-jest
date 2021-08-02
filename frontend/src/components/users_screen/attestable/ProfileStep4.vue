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
        label="Домашний адрес"
        autocomplete="address"
        v-model="$v.form.home_address.$model"
        :error-messages="homeAddressErrors"
        @input="
          $v.form.home_address.$touch();
          sendForm();
        "
        @blur="
          $v.form.home_address.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Мобильный телефон"
        autocomplete="phone"
        v-model="$v.form.personal_phone.$model"
        :error-messages="personalPhoneErrors"
        @input="
          $v.form.personal_phone.$touch();
          sendForm();
        "
        @blur="
          $v.form.personal_phone.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Домашний телефон"
        autocomplete="home_phone"
        v-model="$v.form.home_phone.$model"
        :error-messages="homePhoneErrors"
        @input="
          $v.form.home_phone.$touch();
          sendForm();
        "
        @blur="
          $v.form.home_phone.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Рабочий телефон"
        autocomplete="work_phone"
        v-model="$v.form.work_phone.$model"
        :error-messages="workPhoneErrors"
        @input="
          $v.form.work_phone.$touch();
          sendForm();
        "
        @blur="
          $v.form.work_phone.$touch();
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
// TODO:
// - home_address Домашний адрес
// - !!! email E-mail
// - personal_phone Мобильный телефон
// - home_phone Домашний телефон
// - work_phone Рабочий телефон

import { required } from "vuelidate/lib/validators";
import { SET_FOURTH_PROFILE_PART } from "@/graphql/user_request_mutations.js";
import { GET_FOURTH_PROFILE_PART } from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep4",
  data() {
    return {
      formLoading: false,
      form: {
        home_address: null,
        personal_phone: null,
        home_phone: null,
        work_phone: null
      }
    };
  },
  apollo: {
    user: {
      query: GET_FOURTH_PROFILE_PART,
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
        if (val.homeAddress) {
          this.$v.form.$model.home_address = val.homeAddress;
        }
        if (val.personalPhone) {
          this.$v.form.$model.personal_phone = val.personalPhone;
        }
        if (val.homePhone) {
          this.$v.form.$model.home_phone = val.homePhone;
        }
        if (val.workPhone) {
          this.$v.form.$model.work_phone = val.workPhone;
        }
      }
    }
  },
  validations: {
    form: {
      home_address: { required },
      personal_phone: { required },
      home_phone: { required },
      work_phone: { required }
    }
  },
  computed: {
    homeAddressErrors() {
      const errors = [];
      if (!this.$v.form.home_address.$dirty) return errors;
      !this.$v.form.home_address.required &&
        errors.push("Поле 'Домашний адрес' обязательно!");
      return errors;
    },
    personalPhoneErrors() {
      const errors = [];
      if (!this.$v.form.personal_phone.$dirty) return errors;
      !this.$v.form.personal_phone.required &&
        errors.push("Поле 'Мобильный телефон' обязательно!");
      return errors;
    },
    homePhoneErrors() {
      const errors = [];
      if (!this.$v.form.home_phone.$dirty) return errors;
      !this.$v.form.home_phone.required &&
        errors.push("Поле 'Домашний телефон' обязательно!");
      return errors;
    },
    workPhoneErrors() {
      const errors = [];
      if (!this.$v.form.work_phone.$dirty) return errors;
      !this.$v.form.work_phone.required &&
        errors.push("Поле 'Рабочий телефон' обязательно!");
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
            mutation: SET_FOURTH_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              homeAddress: this.$v.form.$model.home_address,
              personalPhone: this.$v.form.$model.personal_phone,
              homePhone: this.$v.form.$model.home_phone,
              workPhone: this.$v.form.$model.work_phone
            },
            update: (cache, { data: { setFourthProfilePart } }) => {
              const data = cache.readQuery({
                query: GET_FOURTH_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id
                }
              });

              data.user.home_address = setFourthProfilePart.user.home_address;
              data.user.personal_phone =
                setFourthProfilePart.user.personal_phone;
              data.user.home_phone = setFourthProfilePart.user.home_phone;
              data.user.work_phone = setFourthProfilePart.user.work_phone;

              cache.writeQuery({
                query: GET_FOURTH_PROFILE_PART,
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
