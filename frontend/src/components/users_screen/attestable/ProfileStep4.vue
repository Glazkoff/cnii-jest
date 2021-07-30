<template>
  <div>
    <v-progress-circular
      indeterminate
      color="primary"
      v-if="this.$apollo.queries.user.loading"
    >
    </v-progress-circular>
    <v-form ref="form" lazy-validation v-else></v-form>
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
        if (val.home_address) {
          this.$v.form.$model.home_address = val.homeAddress;
        }
        if (val.personal_phone) {
          this.$v.form.$model.personal_phone = val.personalPhone;
        }
        if (val.home_phone) {
          this.$v.form.$model.home_phone = val.homePhone;
        }
        if (val.work_phone) {
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
    // TODO: add computed errors
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
    sendForm() {
      // TODO: add sendForm
    }
  }
};
</script>

<style lang="scss" scoped></style>
