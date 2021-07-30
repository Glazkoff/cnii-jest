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
      workExperienceFullYears
      workExperienceCurrentJob
      awards
      training
      organizationMembership
    }
  }
`;
