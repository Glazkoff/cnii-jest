<template>
  <div>
    <v-form ref="form" lazy-validation>
      <v-text-field
        label="Фамилия"
        autocomplete="surname"
        v-model="$v.form.surname.$model"
        :error-messages="surnameErrors"
        @input="$v.form.surname.$touch()"
        @blur="$v.form.surname.$touch()"
        required
      ></v-text-field>
      <v-text-field
        label="Имя"
        autocomplete="name"
        v-model="$v.form.name.$model"
        :error-messages="nameErrors"
        @input="$v.form.name.$touch()"
        @blur="$v.form.name.$touch()"
        required
      ></v-text-field>
      <v-text-field
        label="Отчество"
        autocomplete="patricity"
        v-model="$v.form.patricity.$model"
        :error-messages="patricityErrors"
        @input="$v.form.patricity.$touch()"
        @blur="$v.form.patricity.$touch()"
        required
      ></v-text-field>
      <DatePicker
        label="Дата рождения"
        autocomplete="date_of_birth"
        @update="$v.form.birthday.$model = $event"
        :disabled="formLoading"
        :errors="dateErrors"
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
        @input="$v.form.sex.$touch()"
        @blur="$v.form.sex.$touch()"
      ></v-select>
    </v-form>
    <v-btn
      class="mt-2"
      color="primary"
      :disabled="$v.form.$anyError"
      @click="goToNextStep"
    >
      Далее
    </v-btn>
  </div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import DatePicker from "../../global/DatePicker.vue";
import { SET_FIRST_PROFILE_PART } from "@/graphql/user_request_mutations.js";

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
      // !this.$v.form.patricity.required && errors.push("Поле обязательно");
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
    }
  },
  methods: {
    goToNextStep() {
      const nextStep = 2;
      this.$v.form.$touch();
      if (this.$v.form.$anyError) {
        console.log("anyError");
      } else {
        console.log("noAnyError");
        this.formLoading = true;
        this.sendFirstStep()
          .then(() => {
            console.log("Next step: ", nextStep);
          })
          .finally(() => {
            this.formLoading = false;
          });
      }
    },
    sendFirstStep() {
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
            }
          })
          .then(res => {
            resolve(res);
            console.log("SEND: ", this.$v.form.$model);
          })
          .catch(err => {
            reject(err);
            console.log("ОШИБКА МУТАЦИИ: ", err);
          });
      });
    }
  }
};
</script>

<style lang="scss" scoped></style>
