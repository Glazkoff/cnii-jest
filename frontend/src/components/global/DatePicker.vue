<template>
  <v-menu
    ref="menu"
    v-model="menu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    max-width="290px"
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="dateFormatted"
        :label="label"
        persistent-hint
        prepend-icon="mdi-calendar"
        v-bind="attrs"
        :autocomplete="autocomplete"
        @blur="
          date = parseDate(dateFormatted);
          $v.dateFormatted.$touch();
        "
        v-on="on"
        color="colorOfSea"
        v-mask="'##.##.####'"
        required
        :error-messages="errors"
        v-model.trim="$v.dateFormatted.$model"
        @input="$v.dateFormatted.$touch()"
      ></v-text-field>
    </template>
    <v-date-picker
      v-model="date"
      no-title
      @input="menu = false"
      color="colorOfSea"
      :max="max"
      :min="min"
    ></v-date-picker>
  </v-menu>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
export default {
  mixins: [validationMixin],
  name: "DatePicker",
  props: ["label", "autocomplete", "errors", "predefined", "max", "min"],
  validations: {
    dateFormatted: {
      required
    }
  },
  data() {
    return {
      date: this.predefined,
      dateFormatted: null,
      menu: false
    };
  },
  computed: {
    computedDateFormatted() {
      return this.formatDate(this.date);
    }
    // dateErrors() {
    // const errors = [];
    //   if (!this.$v.dateFormatted.$dirty) return errors;
    //   !this.$v.dateFormatted.required && errors.push("Укажите дату!");
    //   return errors;
    // }
  },
  watch: {
    date(val) {
      this.dateFormatted = this.formatDate(val);
      let dateEmit = this.parseDate(val);
      this.$emit("update", dateEmit);
    },
    predefined(val) {
      if (val) {
        this.date = val;
        this.$v.dateFormatted.$model = this.formatDate(val);
      }
    }
  },
  mounted() {
    if (this.predefined) {
      this.$v.dateFormatted.$model = this.formatDate(this.predefined);
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },
    parseDate(date) {
      if (!date) return null;
      if (date.split(".").length == 3) {
        const [day, month, year] = date.split(".");
        return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
      } else {
        return date;
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
