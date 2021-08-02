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

// Мутация для отправки данных второго шага
export const SET_SECOND_PROFILE_PART = gql`
  mutation (
    $userId: ID!
    $nativeLanguage: String
    $citizenship: String
    $martialStatus: String
    $organization: String
    $jobPosition: String
    $education: String
  ) {
    setSecondProfilePart(
      userId: $userId
      nativeLanguage: $nativeLanguage
      citizenship: $citizenship
      martialStatus: $martialStatus
      organization: $organization
      jobPosition: $jobPosition
      education: $education
    ) {
      user {
        id
        nativeLanguage
        citizenship
        martialStatus
        organization
        jobPosition
        education
      }
    }
  }
`;

// Мутация для отправки данных третьего шага
export const SET_THIRD_PROFILE_PART = gql`
  mutation (
    $userId: ID!
    $passport: String
    $passportPart1Scan: Upload
    $passportPart2Scan: Upload
  ) {
    setThirdProfilePart(
      userId: $userId
      passport: $passport
      passportPart1Scan: $passportPart1Scan
      passportPart2Scan: $passportPart2Scan
    ) {
      user {
        id
        passport
        passportPart1Scan
        passportPart2Scan
      }
    }
  }
`;

// Мутация для отправки данных четвёртого шага
export const SET_FOURTH_PROFILE_PART = gql`
  mutation (
    $userId: ID!
    $homeAddress: String
    $personalPhone: String
    $homePhone: String
    $workPhone: String
  ) {
    setFourthProfilePart(
      userId: $userId
      homeAddress: $homeAddress
      personalPhone: $personalPhone
      homePhone: $homePhone
      workPhone: $workPhone
    ) {
      user {
        homeAddress
        personalPhone
        homePhone
        workPhone
      }
    }
  }
`;
