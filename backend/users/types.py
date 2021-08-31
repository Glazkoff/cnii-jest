import graphene
from graphene_django.types import DjangoObjectType
from .models import CustomUser, Request, RequestRegister


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
        register = RequestRegister.objects.filter(request=self)
        try:
            if register[0] is not None:
                additional_nulls = ""
                if register[0].order < 10:
                    additional_nulls += "00"
                elif register[0].order < 100:
                    additional_nulls += "0"
                return "06-10-"+additional_nulls+str(register[0].order)
        except IndexError:
            return "-"

    class Meta:
        model = Request
        fields = "__all__"


class RequestRegisterType(DjangoObjectType):
    request_number = graphene.String()

    def resolve_request_number(self, info):
        try:
            if self.order is not None:
                additional_nulls = ""
                if self.order < 10:
                    additional_nulls += "00"
                elif self.order < 100:
                    additional_nulls += "0"
                return "06-10-"+additional_nulls+str(self.order)
        except:
            return "-"

    class Meta:
        model = RequestRegister
        fields = "__all__"
