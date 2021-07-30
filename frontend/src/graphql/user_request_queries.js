import gql from "graphql-tag";

// Запрос данных для первого шага
export const GET_FIRST_PROFILE_PART = gql`
  query ($userId: ID!) {
    user(userId: $userId) {
      id
      surname
      name
      patricity
      birthday
      sex
    }
  }
`;
