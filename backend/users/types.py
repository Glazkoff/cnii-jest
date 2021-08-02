from graphene_django.types import DjangoObjectType
from .models import CustomUser, Request


class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = "__all__"


class RequestType(DjangoObjectType):
    class Meta:
        model = Request
        fields = "__all__"
