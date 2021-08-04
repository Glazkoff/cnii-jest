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
    $photo: Upload
  ) {
    setFirstProfilePart(
      userId: $userId
      surname: $surname
      name: $name
      birthday: $birthday
      sex: $sex
      patricity: $patricity
      photo: $photo
    ) {
      user {
        id
        name
        surname
        patricity
        sex
        birthday
        photo
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
        id
        homeAddress
        personalPhone
        homePhone
        workPhone
      }
    }
  }
`;

// Мутация для отправки данных пятого шага
export const SET_FIFTH_PROFILE_PART = gql`
  mutation (
    $userId: ID!
    $workExperienceFullYears: Int
    $workExperienceCurrentJob: Int
    $awards: String
    $training: String
    $organizationMembership: String
  ) {
    setFifthProfilePart(
      userId: $userId
      workExperienceFullYears: $workExperienceFullYears
      workExperienceCurrentJob: $workExperienceCurrentJob
      awards: $awards
      training: $training
      organizationMembership: $organizationMembership
    ) {
      user {
        id
        workExperienceFullYears
        workExperienceCurrentJob
        awards
        training
        organizationMembership
      }
    }
  }
`;

// Мутация для обновления данных шага
export const UPDATE_REQUEST_STATUS = gql`
  mutation ($requestId: ID!, $statusNumber: Int!) {
    updateRequestStatus(requestId: $requestId, statusNumber: $statusNumber) {
      request {
        id
        status
      }
    }
  }
`;

// Мутация для завершения работы с заявкой для пользователя
export const FINISH_REQUEST = gql`
  mutation ($requestId: ID!) {
    finishRequest(requestId: $requestId) {
      request {
        id
        status
      }
    }
  }
`;
