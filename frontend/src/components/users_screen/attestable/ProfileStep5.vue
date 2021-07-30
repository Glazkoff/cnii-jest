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
// - work_experience_full_years Стаж полных лет
// - work_experience_current_job Стаж настоящей должности
// - awards Наличие наград
// - training Повышение квалификации
// - organization_membership Членство в организациях

import { required } from "vuelidate/lib/validators";
import { GET_FIFTH_PROFILE_PART } from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep5",
  data() {
    return {
      formLoading: false,
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
        if (val.work_experience_full_years) {
          this.$v.form.$model.work_experience_full_years =
            val.work_experience_full_years;
        }
        if (val.work_experience_current_job) {
          this.$v.form.$model.work_experience_current_job =
            val.work_experience_current_job;
        }
        if (val.awards) {
          this.$v.form.$model.awards = val.awards;
        }
        if (val.training) {
          this.$v.form.$model.training = val.training;
        }
        if (val.organization_membership) {
          this.$v.form.$model.organization_membership =
            val.organizationMembership;
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
      organization_membership: { required }
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
