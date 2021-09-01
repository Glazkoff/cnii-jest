"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
# from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
# from documents import views
from dj_rest_auth.registration.views import VerifyEmailView
from allauth.account.views import ConfirmEmailView
from allauth.account.views import confirm_email
import users.views

router = routers.DefaultRouter()
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path(r'api/auth/registration/account-email-verification-sent/',
         users.views.null_view, name='account_email_verification_sent'),
    path('api/auth/registration/account-confirm-email/<key>[-:\w]/',
         ConfirmEmailView.as_view(), name='account_confirm_email'),
    path(r'api/auth/registration/complete/', users.views.complete_view,
         name='account_confirm_complete'),
    path('api/documents/', include('documents.urls')),
    path('api/graphql/', FileUploadGraphQLView.as_view(graphiql=True))
]
