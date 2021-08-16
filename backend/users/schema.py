import graphene
from django.contrib.auth.models import User
from .models import CustomUser, Request
from .types import CustomUserType, RequestType
from .mutations import SetFirstProfilePartMutation, SetSecondProfilePartMutation, SetThirdProfilePartMutation, SetFourthProfilePartMutation, SetFifthProfilePartMutation, SetSixthProfilePartMutation, UpdateRequestStatusMutation, FinishRequestMutation
import graphene_django_optimizer as gql_optimizer


class Query(graphene.ObjectType):
    users = graphene.List(CustomUserType)
    user = graphene.Field(CustomUserType, user_id=graphene.ID())
    request = graphene.Field(RequestType, request_id=graphene.ID())
    user_requests = graphene.List(RequestType, user_id=graphene.ID())

    def resolve_users(self, info, **kwargs):
        return gql_optimizer.query(CustomUser.objects.all(), info)

    def resolve_user(self, info, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except (CustomUser.DoesNotExist,):
            return None

    def resolve_request(self, info, request_id):
        try:
            return Request.objects.get(pk=request_id)
        except:
            return None

    def resolve_user_requests(self, info, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return gql_optimizer.query(Request.objects.filter(user=user), info)
        except:
            return None


class Mutation(graphene.ObjectType):
    set_first_profile_part = SetFirstProfilePartMutation.Field()
    set_second_profile_part = SetSecondProfilePartMutation.Field()
    set_third_profile_part = SetThirdProfilePartMutation.Field()
    set_fourth_profile_part = SetFourthProfilePartMutation.Field()
    set_fifth_profile_part = SetFifthProfilePartMutation.Field()
    set_sixth_profile_part = SetSixthProfilePartMutation.Field()
    update_request_status = UpdateRequestStatusMutation.Field()
    finish_request = FinishRequestMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
