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
      photo
    }
  }
`;

// Запрос данных для второго шага
export const GET_SECOND_PROFILE_PART = gql`
  query ($userId: ID!) {
    user(userId: $userId) {
      id
      nativeLanguage
      citizenship
      martialStatus
      organization
      jobPosition
      education
      mainDiplomaScan
      gestureDiplomaScan
    }
  }
`;

// Запрос данных для третьего шага
export const GET_THIRD_PROFILE_PART = gql`
  query ($userId: ID!) {
    user(userId: $userId) {
      id
      passport
      passportPart1Scan
      passportPart2Scan
    }
  }
`;

// Запрос данных для четвёртого шага
export const GET_FOURTH_PROFILE_PART = gql`
  query ($userId: ID!) {
    user(userId: $userId) {
      id
      homeAddress
      personalPhone
      homePhone
      workPhone
    }
  }
`;

// Запрос данных для пятого шага
export const GET_FIFTH_PROFILE_PART = gql`
  query ($userId: ID!) {
    user(userId: $userId) {
      id
      fullWorkExperienceStartYear
      currentJobExperienceStartYear
      awards
      training
      organizationMembership
      characteristic
      employmentHistory
    }
  }
`;

// Запрос данных для шестого шага
export const GET_SIXTH_PROFILE_PART = gql`
  query ($userId: ID!, $requestId: ID!) {
    user(userId: $userId) {
      id
      attestationCertificateNumber
      attestationCertificateDate
      attestationCertificateScan
    }
    request(requestId: $requestId) {
      id
      cheque
    }
  }
`;

// Запрос списка заявок одного пользователя
export const USER_REQUESTS = gql`
  query ($userId: ID!) {
    userRequests(userId: $userId) {
      id
      requestNumber
      status
      comment
    }
  }
`;

// Запрос данных о текущем статусе заявки
export const REQUEST_STATUS = gql`
  query ($requestId: ID!) {
    request(requestId: $requestId) {
      id
      status
    }
  }
`;

// Запрос данных о чекк заявки
export const REQUEST_CHEQUE = gql`
  query ($requestId: ID!) {
    request(requestId: $requestId) {
      id
      cheque
    }
  }
`;
