<template>
  <div>
    <h1>Ваши заявки</h1>
    <v-data-table :headers="headers" :items="items">
      <template v-slot:item="row">
        <tr>
          <td>
            <b>{{ row.item.requestNumber }}</b>
          </td>
          <td>{{ row.item.status }}</td>
          <td>
            <div class="d-flex justify-end">
              <v-btn
                class="mx-2"
                dark
                color="primary"
                :to="`/request/${row.item.id}`"
              >
                Редактировать <v-icon dark>mdi-arrow-right</v-icon>
              </v-btn>
            </div>
          </td>
        </tr>
      </template>
    </v-data-table>
    <!-- {{ userRequests }} -->
  </div>
</template>

<script>
import { USER_REQUESTS } from "@/graphql/user_request_queries.js";

export default {
  name: "AttestableList",
  data() {
    return {
      headers: [
        {
          text: "Номер заявки",
          value: "requestNumber"
        },
        {
          text: "Статус заявки",
          value: "status"
        },
        {
          text: "Действия",
          value: "actions",
          sortable: false,
          align: "right"
        }
      ]
    };
  },
  apollo: {
    userRequests: {
      query: USER_REQUESTS,
      variables() {
        return {
          userId: this.$store.getters.user_id
        };
      }
    }
  },
  computed: {
    items() {
      if (this.userRequests !== undefined) {
        return this.userRequests.map(el => {
          switch (el.status.toUpperCase()) {
            case "STEP_1":
              el.status = "Шаг 1";
              break;
            case "STEP_2":
              el.status = "Шаг 2";
              break;
            case "STEP_3":
              el.status = "Шаг 3";
              break;
            case "STEP_4":
              el.status = "Шаг 4";
              break;
            case "STEP_5":
              el.status = "Шаг 5";
              break;
            case "STEP_6":
              el.status = "Шаг 6";
              break;
            case "ON_CHECK":
              el.status = "Отправлена на проверку";
              break;
            case "CANCELED":
              el.status = "Отклонена";
              break;
            case "CONFIRMED":
              el.status = "Успешно подтверждена";
              break;
            case "COMPLETED":
              el.status = "Завершена работа";
              break;
            default:
              console.log(el.status);
              el.status = "-";
              break;
          }
          return el;
        });
      } else {
        return this.userRequests;
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
