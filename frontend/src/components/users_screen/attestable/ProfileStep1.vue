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
        label="Фамилия"
        autocomplete="surname"
        v-model="$v.form.surname.$model"
        :error-messages="surnameErrors"
        @input="
          $v.form.surname.$touch();
          sendForm();
        "
        @blur="
          $v.form.surname.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Имя"
        autocomplete="name"
        v-model="$v.form.name.$model"
        :error-messages="nameErrors"
        @input="
          $v.form.name.$touch();
          sendForm();
        "
        @blur="
          $v.form.name.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <v-text-field
        label="Отчество"
        autocomplete="patricity"
        v-model="$v.form.patricity.$model"
        :error-messages="patricityErrors"
        @input="
          $v.form.patricity.$touch();
          sendForm();
        "
        @blur="
          $v.form.patricity.$touch();
          sendForm();
        "
        required
      ></v-text-field>
      <DatePicker
        label="Дата рождения"
        autocomplete="date_of_birth"
        @update="
          $v.form.birthday.$model = $event;
          sendForm();
        "
        :disabled="formLoading"
        :errors="dateErrors"
        :predefined="predefinedBirthday"
        :max="new Date().toISOString().slice(0, 10)"
      ></DatePicker>
      <v-select
        :items="[
          { text: 'Мужской', value: 'M' },
          { text: 'Женский', value: 'F' }
        ]"
        item-text="text"
        item-value="value"
        label="Пол"
        autocomplete="sex"
        v-model="$v.form.sex.$model"
        :error-messages="sexErrors"
        @input="
          $v.form.sex.$touch();
          sendForm();
        "
        @blur="
          $v.form.sex.$touch();
          sendForm();
        "
      ></v-select>
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
  </div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import DatePicker from "../../global/DatePicker.vue";
import { SET_FIRST_PROFILE_PART } from "@/graphql/user_request_mutations.js";
import { GET_FIRST_PROFILE_PART } from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep1",
  components: {
    DatePicker
  },
  data() {
    return {
      formLoading: false,
      form: {
        surname: null,
        name: null,
        patricity: null,
        birthday: null,
        sex: null
      }
    };
  },
  apollo: {
    user: {
      query: GET_FIRST_PROFILE_PART,
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
        if (val.surname) {
          this.$v.form.$model.surname = val.surname;
        }
        if (val.name) {
          this.$v.form.$model.name = val.name;
        }
        if (val.patricity) {
          this.$v.form.$model.patricity = val.patricity;
        }
        if (val.sex) {
          this.$v.form.$model.sex = val.sex;
        }
        if (val.birthday) {
          this.$v.form.$model.birthday = val.birthday;
        }
      }
    }
  },
  validations: {
    form: {
      surname: { required },
      name: { required },
      patricity: {},
      birthday: { required },
      sex: { required }
    }
  },
  computed: {
    surnameErrors() {
      const errors = [];
      if (!this.$v.form.surname.$dirty) return errors;
      !this.$v.form.surname.required &&
        errors.push("Поле 'Фамилия' обязательно!");
      return errors;
    },
    nameErrors() {
      const errors = [];
      if (!this.$v.form.name.$dirty) return errors;
      !this.$v.form.name.required && errors.push("Поле 'Имя' обязательно!");
      return errors;
    },
    patricityErrors() {
      const errors = [];
      if (!this.$v.form.patricity.$dirty) return errors;
      return errors;
    },
    sexErrors() {
      const errors = [];
      if (!this.$v.form.sex.$dirty) return errors;
      !this.$v.form.sex.required && errors.push("Поле 'Пол' обязательно");
      return errors;
    },
    dateErrors() {
      const errors = [];
      if (!this.$v.form.birthday.$dirty) return errors;
      !this.$v.form.birthday.required &&
        errors.push("Поле 'Дата рождения' обязательно");
      return errors;
    },
    predefinedBirthday() {
      if (this.user) {
        if (this.user.birthday) {
          return this.user.birthday;
        } else {
          return null;
        }
      } else {
        return null;
      }
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
    sendForm() {
      return new Promise((resolve, reject) => {
        this.$apollo
          .mutate({
            mutation: SET_FIRST_PROFILE_PART,
            variables: {
              userId: this.$store.getters.decoded.user_id,
              surname: this.$v.form.$model.surname,
              name: this.$v.form.$model.name,
              birthday: this.$v.form.$model.birthday,
              sex: this.$v.form.$model.sex,
              patricity: this.$v.form.$model.patricity
            },
            update: (cache, { data: { setFirstProfilePart } }) => {
              const data = cache.readQuery({
                query: GET_FIRST_PROFILE_PART,
                variables: {
                  userId: this.$store.getters.user_id
                }
              });

              data.user.surname = setFirstProfilePart.user.surname;
              data.user.name = setFirstProfilePart.user.name;
              data.user.patricity = setFirstProfilePart.user.patricity;
              data.user.birthday = setFirstProfilePart.user.birthday;
              data.user.sex = setFirstProfilePart.user.sex;

              cache.writeQuery({
                query: GET_FIRST_PROFILE_PART,
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
