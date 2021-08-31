from transliterate import translit
from django.core.files.base import ContentFile, File
import os
import datetime
import graphene
from django.contrib.auth.models import User
from .models import CustomUser, Request, RequestRegister, LastRequestOrder
from .types import CustomUserType, RequestType, RequestRegisterType
from graphene_file_upload.scalars import Upload
from django.core.mail import send_mail


class SetFirstProfilePartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        surname = graphene.String()
        name = graphene.String()
        patricity = graphene.String()
        birthday = graphene.Date()
        sex = graphene.String()
        photo = Upload()

    user = graphene.Field(CustomUserType)

    @classmethod
    def mutate(cls, root, info, user_id, surname=None, name=None, birthday=None, sex=None, patricity=None, photo=None):
        try:
            user = User.objects.get(pk=user_id)
            custom_user = CustomUser.objects.get_or_create(user=user)
            if surname is not None:
                custom_user[0].surname = surname
            if name is not None:
                custom_user[0].name = name
            if birthday is not None:
                custom_user[0].birthday = birthday
            if sex is not None:
                custom_user[0].sex = sex
            if patricity is not None:
                custom_user[0].patricity = patricity
            if photo is not None:
                now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
                filename, extension = os.path.splitext(
                    photo.name)
                surname = translit(
                    custom_user[0].surname, language_code='ru', reversed=True)
                name = translit(
                    custom_user[0].name, language_code='ru', reversed=True)
                patricity = translit(
                    custom_user[0].patricity, language_code='ru', reversed=True)
                new_filename = f"{surname}_{name}_{patricity}_photo_{now}{extension}"
                custom_user[0].photo.save(
                    new_filename, File(photo))
            custom_user[0].save()

            return SetFirstProfilePartMutation(user=custom_user[0])
        except (User.DoesNotExist,):
            return SetFirstProfilePartMutation(user=None)


class SetSecondProfilePartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        native_language = graphene.String()
        citizenship = graphene.String()
        martial_status = graphene.String()
        organization = graphene.String()
        job_position = graphene.String()
        education = graphene.String()
        main_diploma_scan = Upload()
        gesture_diploma_scan = Upload()

    user = graphene.Field(CustomUserType)

    @classmethod
    def mutate(cls, root, info, user_id, native_language=None, citizenship=None, martial_status=None, organization=None, job_position=None, education=None, main_diploma_scan=None, gesture_diploma_scan=None):
        try:
            user = User.objects.get(pk=user_id)
            custom_user = CustomUser.objects.get_or_create(user=user)
            if native_language is not None:
                custom_user[0].native_language = native_language
            if citizenship is not None:
                custom_user[0].citizenship = citizenship
            if martial_status is not None:
                custom_user[0].martial_status = martial_status
            if organization is not None:
                custom_user[0].organization = organization
            if job_position is not None:
                custom_user[0].job_position = job_position
            if education is not None:
                custom_user[0].education = education
            now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
            if main_diploma_scan is not None:
                filename, extension = os.path.splitext(
                    main_diploma_scan.name)
                surname = translit(
                    custom_user[0].surname, language_code='ru', reversed=True)
                name = translit(
                    custom_user[0].name, language_code='ru', reversed=True)
                patricity = translit(
                    custom_user[0].patricity, language_code='ru', reversed=True)
                new_filename = f"{surname}_{name}_{patricity}_main_diploma_{now}{extension}"
                custom_user[0].main_diploma_scan.save(
                    new_filename, File(main_diploma_scan))
            if gesture_diploma_scan is not None:
                filename, extension = os.path.splitext(
                    gesture_diploma_scan.name)
                surname = translit(
                    custom_user[0].surname, language_code='ru', reversed=True)
                name = translit(
                    custom_user[0].name, language_code='ru', reversed=True)
                patricity = translit(
                    custom_user[0].patricity, language_code='ru', reversed=True)
                new_filename = f"{surname}_{name}_{patricity}_gesture_diploma_{now}{extension}"
                custom_user[0].gesture_diploma_scan.save(
                    new_filename, File(gesture_diploma_scan))
            custom_user[0].save()

            return SetSecondProfilePartMutation(user=custom_user[0])
        except (User.DoesNotExist,):
            return SetSecondProfilePartMutation(user=None)


class SetThirdProfilePartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        passport = graphene.String()
        passport_part1_scan = Upload()
        passport_part2_scan = Upload()

    user = graphene.Field(CustomUserType)

    @classmethod
    def mutate(cls, root, info, user_id, passport=None, passport_part1_scan=None, passport_part2_scan=None):
        try:
            user = User.objects.get(pk=user_id)
            custom_user = CustomUser.objects.get_or_create(user=user)
            if passport is not None:
                custom_user[0].passport = passport
            now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
            if passport_part1_scan is not None:
                filename, extension = os.path.splitext(
                    passport_part1_scan.name)
                surname = translit(
                    custom_user[0].surname, language_code='ru', reversed=True)
                name = translit(
                    custom_user[0].name, language_code='ru', reversed=True)
                patricity = translit(
                    custom_user[0].patricity, language_code='ru', reversed=True)
                new_filename = f"{surname}_{name}_{patricity}_passport_part1_{now}{extension}"
                custom_user[0].passport_part1_scan.save(
                    new_filename, File(passport_part1_scan))
            if passport_part2_scan is not None:
                filename, extension = os.path.splitext(
                    passport_part2_scan.name)
                surname = translit(
                    custom_user[0].surname, language_code='ru', reversed=True)
                name = translit(
                    custom_user[0].name, language_code='ru', reversed=True)
                patricity = translit(
                    custom_user[0].patricity, language_code='ru', reversed=True)
                new_filename = f"{surname}_{name}_{patricity}_passport_part2_{now}{extension}"
                custom_user[0].passport_part2_scan.save(
                    new_filename, File(passport_part2_scan))
            custom_user[0].save()
            return SetThirdProfilePartMutation(user=custom_user[0])
        except (User.DoesNotExist,):
            return SetThirdProfilePartMutation(user=None)


class SetFourthProfilePartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        home_address = graphene.String()
        personal_phone = graphene.String()
        home_phone = graphene.String()
        work_phone = graphene.String()

    user = graphene.Field(CustomUserType)

    @classmethod
    def mutate(cls, root, info, user_id, home_address=None, personal_phone=None, home_phone=None, work_phone=None,):
        try:
            user = User.objects.get(pk=user_id)
            custom_user = CustomUser.objects.get_or_create(user=user)
            if home_address is not None:
                custom_user[0].home_address = home_address
            if personal_phone is not None:
                custom_user[0].personal_phone = personal_phone
            if home_phone is not None:
                custom_user[0].home_phone = home_phone
            if work_phone is not None:
                custom_user[0].work_phone = work_phone
            custom_user[0].save()

            return SetFourthProfilePartMutation(user=custom_user[0])
        except (User.DoesNotExist,):
            return SetFourthProfilePartMutation(user=None)


class SetFifthProfilePartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        full_work_experience_start_year = graphene.Int()
        current_job_experience_start_year = graphene.Int()
        awards = graphene.String()
        training = graphene.String()
        organization_membership = graphene.String()
        characteristic = Upload()
        employment_history = Upload()

    user = graphene.Field(CustomUserType)

    @classmethod
    def mutate(cls, root, info, user_id, full_work_experience_start_year=None, current_job_experience_start_year=None, awards=None, training=None, organization_membership=None, characteristic=None, employment_history=None):
        try:
            now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
            user = User.objects.get(pk=user_id)
            custom_user = CustomUser.objects.get_or_create(user=user)
            if full_work_experience_start_year is not None:
                custom_user[0].full_work_experience_start_year = full_work_experience_start_year
            if current_job_experience_start_year is not None:
                custom_user[0].current_job_experience_start_year = current_job_experience_start_year
            if awards is not None:
                custom_user[0].awards = awards
            if training is not None:
                custom_user[0].training = training
            if organization_membership is not None:
                custom_user[0].organization_membership = organization_membership
            if characteristic is not None:
                filename, extension = os.path.splitext(
                    characteristic.name)
                surname = translit(
                    custom_user[0].surname, language_code='ru', reversed=True)
                name = translit(
                    custom_user[0].name, language_code='ru', reversed=True)
                patricity = translit(
                    custom_user[0].patricity, language_code='ru', reversed=True)
                new_filename = f"{surname}_{name}_{patricity}_characteristic_{now}{extension}"
                custom_user[0].characteristic.save(
                    new_filename, File(characteristic))
            if employment_history is not None:
                filename, extension = os.path.splitext(
                    employment_history.name)
                surname = translit(
                    custom_user[0].surname, language_code='ru', reversed=True)
                name = translit(
                    custom_user[0].name, language_code='ru', reversed=True)
                patricity = translit(
                    custom_user[0].patricity, language_code='ru', reversed=True)
                new_filename = f"{surname}_{name}_{patricity}_employment_history_{now}{extension}"
                custom_user[0].employment_history.save(
                    new_filename, File(employment_history))
            custom_user[0].save()
            return SetFifthProfilePartMutation(user=custom_user[0])
        except (User.DoesNotExist,):
            return SetFifthProfilePartMutation(user=None)


class SetSixthProfilePartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        request_id = graphene.ID(required=True)
        attestation_certificate_number = graphene.String()
        attestation_certificate_date = graphene.Date()
        attestation_certificate_scan = Upload()
        cheque = Upload()

    user = graphene.Field(CustomUserType)
    request = graphene.Field(RequestType)

    @classmethod
    def mutate(cls, root, info, user_id, request_id, attestation_certificate_number=None, attestation_certificate_date=None, attestation_certificate_scan=None, cheque=None):
        try:
            now = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
            user = User.objects.get(pk=user_id)
            custom_user = CustomUser.objects.get_or_create(user=user)
            request = Request.objects.get(pk=request_id)
            surname = translit(
                custom_user[0].surname, language_code='ru', reversed=True)
            name = translit(
                custom_user[0].name, language_code='ru', reversed=True)
            patricity = translit(
                custom_user[0].patricity, language_code='ru', reversed=True)
            if attestation_certificate_number is not None:
                custom_user[0].attestation_certificate_number = attestation_certificate_number
            if attestation_certificate_date is not None:
                custom_user[0].attestation_certificate_date = attestation_certificate_date
            if attestation_certificate_scan is not None:
                filename, extension = os.path.splitext(
                    attestation_certificate_scan.name)
                new_filename = f"{surname}_{name}_{patricity}_attestation_certificate_{now}{extension}"
                custom_user[0].attestation_certificate_scan.save(
                    new_filename, File(attestation_certificate_scan))
            if cheque is not None:
                filename, extension = os.path.splitext(
                    cheque.name)
                new_filename = f"{surname}_{name}_{patricity}_cheque_{now}{extension}"
                request.cheque.save(
                    new_filename, File(cheque))
                request.save()
            custom_user[0].save()
            return SetSixthProfilePartMutation(user=custom_user[0], request=request)
        except (User.DoesNotExist,):
            return SetSixthProfilePartMutation(user=None, request=None)


class UpdateRequestStatusMutation(graphene.Mutation):
    class Arguments:
        request_id = graphene.ID()
        status_number = graphene.Int()

    request = graphene.Field(RequestType)

    @classmethod
    def mutate(cls, root, info, request_id, status_number):
        try:
            request = Request.objects.get(pk=request_id)
            if status_number == 1:
                request.status = "step_1"
            if status_number == 2:
                request.status = "step_2"
            if status_number == 3:
                request.status = "step_3"
            if status_number == 4:
                request.status = "step_4"
            if status_number == 5:
                request.status = "step_5"
            if status_number == 6:
                request.status = "step_6"
            request.save()
            return UpdateRequestStatusMutation(request=request)
        except:
            return UpdateRequestStatusMutation(request=None)


class FinishRequestMutation(graphene.Mutation):
    class Arguments:
        request_id = graphene.ID()

    request = graphene.Field(RequestType)
    register = graphene.Field(RequestRegisterType)

    @classmethod
    def mutate(cls, root, info, request_id):
        try:
            request = Request.objects.get(pk=request_id)
            request.status = "on_check"
            request.save()
            last_request_order = LastRequestOrder.objects.get_or_create(pk=1)[
                0]
            last_request_order.last_order = last_request_order.last_order+1
            last_request_order.save()
            request_register_count = RequestRegister.objects.filter(
                request=request).count()
            if request_register_count == 0:
                request_register = RequestRegister.objects.create(
                    request=request, order=last_request_order.last_order)
            else:
                request_register = RequestRegister.objects.get(request=request)

            created_at_formatted = request.created_at.strftime(
                "%d.%m.%Y %H:%M:%S")
            register = request_register.__str__()

            mail_topic = f'Заявка на аттестацию {register}'
            mail_body = f"Создана новая заявка от {created_at_formatted} ({register})"
            mail_from = "notify@nglazkov.ru"
            mail_to = ['zitrnik@gmail.com']

            send_mail(mail_topic, mail_body,
                      mail_from, mail_to, fail_silently=False)
            return FinishRequestMutation(request=request, register=request_register)
        except:
            return FinishRequestMutation(request=None, register=None)


class StartNewRequestMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID()

    request = graphene.Field(RequestType)

    @classmethod
    def mutate(cls, root, info, user_id):
        try:
            user = User.objects.get(pk=user_id)
            custom_user = CustomUser.objects.get_or_create(user=user)
            request = Request.objects.create(user=custom_user[0])
            return StartNewRequestMutation(request=request)
        except:
            return StartNewRequestMutation(request=None)


class DeleteRequestMutation(graphene.Mutation):
    class Arguments:
        request_id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, request_id):
        try:
            request = Request.objects.get(pk=request_id)
            request.delete()
            return DeleteRequestMutation(cls(ok=False))
        except:
            return DeleteRequestMutation(cls(ok=True))
