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
    $mainDiplomaScan: Upload
    $gestureDiplomaScan: Upload
  ) {
    setSecondProfilePart(
      userId: $userId
      nativeLanguage: $nativeLanguage
      citizenship: $citizenship
      martialStatus: $martialStatus
      organization: $organization
      jobPosition: $jobPosition
      education: $education
      mainDiplomaScan: $mainDiplomaScan
      gestureDiplomaScan: $gestureDiplomaScan
    ) {
      user {
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
    $fullWorkExperienceStartYear: Int
    $currentJobExperienceStartYear: Int
    $awards: String
    $training: String
    $organizationMembership: String
    $characteristic: Upload
    $employmentHistory: Upload
  ) {
    setFifthProfilePart(
      userId: $userId
      fullWorkExperienceStartYear: $fullWorkExperienceStartYear
      currentJobExperienceStartYear: $currentJobExperienceStartYear
      awards: $awards
      training: $training
      organizationMembership: $organizationMembership
      characteristic: $characteristic
      employmentHistory: $employmentHistory
    ) {
      user {
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
  }
`;

// Мутация для отправки данных шестого шага
export const SET_SIXTH_PROFILE_PART = gql`
  mutation (
    $userId: ID!
    $requestId: ID!
    $attestationCertificateNumber: String
    $attestationCertificateDate: Date
    $attestationCertificateScan: Upload
    $cheque: Upload
  ) {
    setSixthProfilePart(
      userId: $userId
      requestId: $requestId
      attestationCertificateNumber: $attestationCertificateNumber
      attestationCertificateDate: $attestationCertificateDate
      attestationCertificateScan: $attestationCertificateScan
      cheque: $cheque
    ) {
      user {
        id
        attestationCertificateNumber
        attestationCertificateDate
        attestationCertificateScan
      }
      request {
        id
        status
        cheque
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
      register {
        id
        requestNumber
      }
    }
  }
`;

// Мутация для создания новой заявки
export const START_NEW_REQUEST = gql`
  mutation ($userId: ID!) {
    startNewRequest(userId: $userId) {
      request {
        id
        requestNumber
        status
      }
    }
  }
`;

// Мутация для удаления заявки
export const DELETE_REQUEST = gql`
  mutation ($requestId: ID!) {
    deleteRequest(requestId: $requestId) {
      ok
    }
  }
`;
