<template>
  <v-flex class="auth-form text-center">
    <SuccessSignUpDialog
      @close="$store.commit('CLOSE_SIGN_UP_DIALOG')"
    ></SuccessSignUpDialog>
    <h1 class="mb-12">Авторизация</h1>
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
            "
            @blur="
              $v.form.email.$touch();
              requestErrors = [];
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
            autocomplete="current-password"
            required
            :error-messages="passwordErrors"
            v-model.trim="$v.form.password.$model"
            @input="
              $v.form.password.$touch();
              requestErrors = [];
            "
            @blur="
              $v.form.password.$touch();
              requestErrors = [];
            "
          ></v-text-field>
          <v-btn
            class="mt-8 my-button wide-padding white--text"
            color="primary"
            @click.prevent="logIn"
            block="block"
            type="submit"
            :disabled="$v.form.$invalid || formLoading"
            :loading="formLoading"
          >
            Войти
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <div class="darkBlue--text">
      Ещё нет аккаунта?
      <router-link class="link" :to="'/signup'" :disabled="formLoading"
        >Зарегистрируйтесь!</router-link
      >
    </div>
  </v-flex>
</template>

<script>
import { required, email } from "vuelidate/lib/validators";
import SuccessSignUpDialog from "./SuccessSignUpDialog.vue";

export default {
  name: "LogIn",
  components: {
    SuccessSignUpDialog
  },
  data() {
    return {
      passShow: false,
      formLoading: false,
      form: {
        email: "",
        password: ""
      },
      requestErrors: []
    };
  },
  validations: {
    form: {
      email: {
        required,
        email
      },
      password: {
        required
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
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.form.password.$dirty) return errors;
      !this.$v.form.password.required && errors.push("Укажите пароль!");
      this.requestErrors.length > 0 &&
        this.requestErrors.forEach(element => {
          errors.push(element);
        });
      return errors;
    }
  },
  methods: {
    logIn() {
      let sendObj = { ...this.form };
      this.formLoading = true;
      this.$store.dispatch("LOG_IN", sendObj).then(
        () => {
          this.formLoading = false;
          this.$router.push("/");
        },
        errors => {
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
        }
      );
    }
  }
};
</script>

<style lang="scss" scoped></style>
