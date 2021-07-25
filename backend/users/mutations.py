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
