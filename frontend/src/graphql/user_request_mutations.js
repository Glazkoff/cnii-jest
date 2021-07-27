import gql from "graphql-tag";

// Мутация для отправки данных первого шага
export const SET_FIRST_PROFILE_PART = gql`
  mutation (
    $userId: ID!
    $surname: String
    $name: String
    $birthday: Date
    $sex: String
    $patricity: String
  ) {
    setFirstProfilePart(
      userId: $userId
      surname: $surname
      name: $name
      birthday: $birthday
      sex: $sex
      patricity: $patricity
    ) {
      user {
        id
        name
        surname
        patricity
        sex
        birthday
      }
    }
  }
`;
