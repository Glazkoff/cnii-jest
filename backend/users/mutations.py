from transliterate import translit
from django.core.files.base import ContentFile, File
import os
import datetime
import graphene
from django.contrib.auth.models import User
from .models import CustomUser
from .types import CustomUserType
from graphene_file_upload.scalars import Upload


class SetFirstProfilePartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        surname = graphene.String()
        name = graphene.String()
        patricity = graphene.String()
        birthday = graphene.Date()
        sex = graphene.String()

    user = graphene.Field(CustomUserType)

    @classmethod
    def mutate(cls, root, info, user_id, surname=None, name=None, birthday=None, sex=None, patricity=None):
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

    user = graphene.Field(CustomUserType)

    @classmethod
    def mutate(cls, root, info, user_id, native_language=None, citizenship=None, martial_status=None, organization=None, job_position=None, education=None):
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