<template>
  <div>
    <div v-if="this.$apollo.queries.user.loading || circleLoading">
      <v-progress-circular indeterminate color="primary"> </v-progress-circular>
    </div>
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
      <div v-if="user.photo && !uploadPhoto">
        <small>Ваше фото</small><br />
        <v-btn
          color="success"
          text
          block
          small
          @click="
            uploadPhoto = true;
            user.photo = null;
            $v.form.photo.$model = null;
          "
        >
          Выбрать другой файл
        </v-btn>
        <v-img
          :src="`/media/${user.photo}`"
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
        placeholder="Прикрепите ваше фото"
        label="Ваше фото"
        prepend-icon="mdi-camera"
        :messages="[
          'Загрузите в формате png, jpeg, jpg, pjp, pjpeg, jfif, bmp'
        ]"
        class="mb-2"
        :error-messages="photoErrors"
        v-model="$v.form.photo.$model"
        @input="
          $v.form.photo.$touch();
          sendForm();
        "
        @blur="
          $v.form.photo.$touch();
          sendForm();
        "
      ></v-file-input>
    </v-form>
    <v-btn
      class="mt-2"
      color="primary"
      :disabled="$v.form.$anyError"
      @click="goToNextStep"
      v-if="!this.$apollo.queries.user.loading && !circleLoading"
    >
      Далее
    </v-btn>
  </div>
</template>

<script>
import { required, requiredIf } from "vuelidate/lib/validators";
import DatePicker from "../../global/DatePicker.vue";
import {
  SET_FIRST_PROFILE_PART,
  UPDATE_REQUEST_STATUS
} from "@/graphql/user_request_mutations.js";
import { GET_FIRST_PROFILE_PART } from "@/graphql/user_request_queries.js";

export default {
  name: "ProfileStep1",
  components: {
    DatePicker
  },
  data() {
    return {
      formLoading: false,
      circleLoading: false,
      uploadPhoto: false,
      form: {
        surname: null,
        name: null,
        patricity: null,
        birthday: null,
        sex: null,
        photo: null
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
      sex: { required },
      photo: {
        required: requiredIf(function () {
          return !this.user.photo || this.uploadPhoto;
        })
      }
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
    photoErrors() {
      const errors = [];
      if (!this.$v.form.photo.$dirty) return errors;
      !this.$v.form.photo.required &&
        !(this.user.photo || !this.uploadPhoto) &&
        errors.push("Поле 'Фото' обязательно");
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
            this.sendCurrentStep(2).finally(() => {
              this.$emit("goToNextStep");
              this.formLoading = false;
            });
          })
          .catch(() => {
            this.formLoading = false;
          });
      }
    },
    sendForm() {
      if (this.$v.form.$model.photo) {
        this.uploadPhoto = false;
      }
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
              patricity: this.$v.form.$model.patricity,
              photo: this.$v.form.$model.photo
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
              data.user.photo = setFirstProfilePart.user.photo;

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
