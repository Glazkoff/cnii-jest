<template>
  <v-flex class="auth-form text-center">
    <h1 class="mb-12">Регистрация</h1>
    <v-card flat light="light">
      <v-card-text>
        <v-form>
          <v-text-field
            outlined
            :disabled="formLoading"
            light="light"
            label="E-mail"
            type="email"
            color="primary"
            autocomplete="email"
            required
            :error-messages="emailErrors"
            v-model.trim="$v.form.email.$model"
            @input="
              $v.form.email.$touch();
              requestErrors = [];
              requestEmailErrors = [];
            "
            @blur="
              $v.form.email.$touch();
              requestErrors = [];
              requestEmailErrors = [];
            "
          ></v-text-field>
          <v-text-field
            outlined
            :disabled="formLoading"
            light="light"
            label="Пароль"
            :type="passShow ? 'text' : 'password'"
            color="primary"
            :append-icon="passShow ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="passShow = !passShow"
            autocomplete="new-password"
            required
            counter
            error-count="3"
            :error-messages="password1Errors"
            v-model.trim="$v.form.password1.$model"
            @input="
              $v.form.password1.$touch();
              requestErrors = [];
              requestPassword1Errors = [];
            "
            @blur="
              $v.form.password1.$touch();
              requestErrors = [];
              requestPassword1Errors = [];
            "
          ></v-text-field>
          <v-text-field
            outlined
            :disabled="formLoading"
            light="light"
            label="Повторите пароль"
            :type="pass2Show ? 'text' : 'password'"
            color="primary"
            :append-icon="pass2Show ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="pass2Show = !pass2Show"
            autocomplete="new-password"
            required
            counter
            error-count="3"
            :error-messages="password2Errors"
            v-model.trim="$v.form.password2.$model"
            @input="
              $v.form.password2.$touch();
              requestErrors = [];
              requestPassword2Errors = [];
            "
            @blur="
              $v.form.password2.$touch();
              requestErrors = [];
              requestPassword2Errors = [];
            "
          ></v-text-field>
          <v-btn
            class="mt-8 my-button wide-padding white--text"
            color="primary"
            @click.prevent="signUp"
            block="block"
            type="submit"
            :disabled="$v.form.$invalid || formLoading"
            :loading="formLoading"
          >
            Зарегистрироваться
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <div class="darkBlue--text">
      Уже есть аккаунт?
      <router-link class="link" :to="'/login'" :disabled="formLoading"
        >Войдите!</router-link
      >
    </div>
  </v-flex>
</template>

<script>
import { required, email, sameAs, minLength } from "vuelidate/lib/validators";

export default {
  name: "SignUp",
  data() {
    return {
      passShow: false,
      pass2Show: false,
      formLoading: false,
      form: {
        email: "",
        password1: "",
        password2: ""
      },
      requestErrors: [],
      requestEmailErrors: [],
      requestPassword1Errors: [],
      requestPassword2Errors: []
    };
  },
  validations: {
    form: {
      email: {
        required,
        email
      },
      password1: {
        required,
        minLength: minLength(8)
      },
      password2: {
        required,
        sameAsPassword: sameAs("password1")
      }
    }
  },
  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.form.email.$dirty) return errors;
      !this.$v.form.email.email && errors.push("Введите корректный e-mail");
      !this.$v.form.email.required && errors.push("Укажите ваш e-mail");
      this.requestErrors.length > 0 &&
        this.requestErrors.forEach(element => {
          errors.push(element);
        });
      this.requestEmailErrors.length > 0 &&
        this.requestEmailErrors.forEach(element => {
          errors.push(element);
        });
      return errors;
    },
    password1Errors() {
      const errors = [];
      if (!this.$v.form.password1.$dirty) return errors;
      !this.$v.form.password1.required && errors.push("Укажите пароль!");
      !this.$v.form.password1.minLength &&
        errors.push("Пароль должен содержать минимум 8 символов!");
      this.requestErrors.length > 0 &&
        this.requestErrors.forEach(element => {
          errors.push(element);
        });
      this.requestPassword1Errors.length > 0 &&
        this.requestPassword1Errors.forEach(element => {
          errors.push(element);
        });
      return errors;
    },
    password2Errors() {
      const errors = [];
      if (!this.$v.form.password2.$dirty) return errors;
      !this.$v.form.password2.required && errors.push("Укажите пароль!");
      !this.$v.form.password2.sameAsPassword &&
        errors.push("Пароли должны совпадать!");
      this.requestErrors.length > 0 &&
        this.requestErrors.forEach(element => {
          errors.push(element);
        });
      this.requestPassword2Errors.length > 0 &&
        this.requestPassword2Errors.forEach(element => {
          errors.push(element);
        });
      return errors;
    }
  },
  methods: {
    signUp() {
      let sendObj = { ...this.form };
      this.formLoading = true;
      this.$store.dispatch("SIGN_UP", sendObj).then(
        () => {
          this.formLoading = false;
          this.$store.commit("OPEN_SIGN_UP_DIALOG");
          this.$router.push("/login");
        },
        errors => {
          console.log("errors: ", errors);
          this.formLoading = false;
          if (errors.non_field_errors) {
            for (
              let index = 0;
              index < errors.non_field_errors.length;
              index++
            ) {
              this.requestErrors.push(errors.non_field_errors[index]);
            }
          }
          if (errors.email) {
            for (let index = 0; index < errors.email.length; index++) {
              this.requestEmailErrors.push(errors.email[index]);
            }
          }
          if (errors.password1) {
            for (let index = 0; index < errors.password1.length; index++) {
              this.requestPassword1Errors.push(errors.password1[index]);
            }
          }
          if (errors.password2) {
            for (let index = 0; index < errors.password2.length; index++) {
              this.requestPassword2Errors.push(errors.password2[index]);
            }
          }
        }
      );
    }
  }
};
</script>

<style lang="scss" scoped></style>
