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
// - passport Данные паспорта
// - passport_part1_scan Скан паспорта (часть 1)
// - passport_part2_scan Скан паспорта (часть 2)

import { required } from "vuelidate/lib/validators";
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
        if (val.passport_part1_scan) {
          this.$v.form.$model.passport_part1_scan = val.passportPart1Scan;
        }
        if (val.passport_part2_scan) {
          this.$v.form.$model.passport_part2_scan = val.passportPart2Scan;
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
