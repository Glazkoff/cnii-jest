<template>
  <div>
    <SendingConfirmationDialog
      @close="$store.commit('CLOSE_SUCCESS_DIALOG')"
    ></SendingConfirmationDialog>
    <h1>Ваши заявки</h1>
    <v-btn
      color="primary"
      class="mt-2 mb-2"
      block
      outlined
      @click="startNewRequest"
    >
      Подать новую заявку
    </v-btn>
    <v-data-table
      :headers="headers"
      :items="items"
      no-data-text="Заявки отсутствуют"
    >
      <template v-slot:item="row">
        <tr>
          <td>
            <b>{{ row.item.requestNumber }}</b>
          </td>
          <td>{{ row.item.status }}</td>
          <td
            v-if="row.item.comment"
            style="max-width: 200px; word-wrap: break-word"
          >
            {{ row.item.comment }}
          </td>
          <td v-else>-</td>
          <td>
            <div class="d-flex justify-end" v-if="canBeEdited(row.item.id)">
              <v-btn
                class="mx-2"
                dark
                color="primary"
                :to="`/request/${row.item.id}`"
              >
                Редактировать <v-icon dark>mdi-arrow-right</v-icon>
              </v-btn>
              <v-btn icon tile depressed @click="deleteRequest(row.item.id)">
                <v-icon dark> mdi-delete </v-icon>
              </v-btn>
            </div>
            <div v-else>-</div>
          </td>
        </tr>
      </template>
    </v-data-table>
    <!-- {{ userRequests }} -->
  </div>
</template>

<script>
import { USER_REQUESTS } from "@/graphql/user_request_queries.js";
import {
  START_NEW_REQUEST,
  DELETE_REQUEST
} from "@/graphql/user_request_mutations.js";
import SendingConfirmationDialog from "./SendingConfirmationDialog";

export default {
  name: "AttestableList",
  components: {
    SendingConfirmationDialog
  },
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
          text: "Комментарий",
          value: "comment",
          sortable: false
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
        let reqArr = JSON.parse(JSON.stringify(this.userRequests));
        if (Array.isArray(reqArr)) {
          return reqArr.map(el => {
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
              case "RETURNED":
                el.status = "Возвращена на доработку";
                break;
              default:
                el.status = "-";
                break;
            }
            return el;
          });
        } else {
          return [];
        }
      } else {
        return this.userRequests;
      }
    },
    showSuccessDialog() {
      return this.$store.state.successRequestDialog;
    }
  },
  methods: {
    startNewRequest() {
      this.$apollo
        .mutate({
          mutation: START_NEW_REQUEST,
          variables: { userId: this.$store.getters.user_id },
          update: (cache, { data: { startNewRequest } }) => {
            let data = cache.readQuery({
              query: USER_REQUESTS,
              variables: {
                userId: this.$store.getters.user_id
              }
            });
            if (Array.isArray(data.userRequests)) {
              data.userRequests.push(startNewRequest.request);
            }
            cache.writeQuery({
              query: USER_REQUESTS,
              variables: {
                userId: this.$store.getters.user_id
              },
              data
            });
          }
        })
        .then(res => {
          if (res.data.startNewRequest != null) {
            this.$router.push(
              `/request/${res.data.startNewRequest.request.id}`
            );
          }
        });
    },
    deleteRequest(requestId) {
      this.$apollo.mutate({
        mutation: DELETE_REQUEST,
        variables: { requestId },
        update: cache => {
          let data = cache.readQuery({
            query: USER_REQUESTS,
            variables: {
              userId: this.$store.getters.user_id
            }
          });
          let index = data.userRequests.findIndex(el => {
            return el.id == requestId;
          });
          if (index != -1) {
            data.userRequests.splice(index, 1);
          }
          cache.writeQuery({
            query: USER_REQUESTS,
            variables: {
              userId: this.$store.getters.user_id
            },
            data
          });
        }
      });
    },
    canBeEdited(requestId) {
      let request = this.userRequests.find(el => el.id == requestId);
      let status = "";
      if (request != null) {
        status = request.status;
      }
      let canBe = false;
      switch (status.toUpperCase()) {
        case "STEP_1":
        case "STEP_2":
        case "STEP_3":
        case "STEP_4":
        case "STEP_5":
        case "STEP_6":
        case "RETURNED":
          canBe = true;
          break;
        case "ON_CHECK":
        case "CANCELED":
        case "CONFIRMED":
        case "COMPLETED":
        default:
          break;
      }
      return canBe;
    }
  }
};
</script>

<style lang="scss" scoped></style>
