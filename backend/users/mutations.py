import graphene
from django.contrib.auth.models import User
from .models import CustomUser
from .types import CustomUserType


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
