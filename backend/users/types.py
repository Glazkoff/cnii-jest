import graphene
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
    request_number = graphene.String()

    def resolve_request_number(self, info):
        additional_nulls = ""
        if self.id < 10:
            additional_nulls += "00"
        elif self.id < 100:
            additional_nulls += "0"
        return "06-10-"+additional_nulls+str(self.id)

    class Meta:
        model = Request
        fields = "__all__"
