# from django.urls import path
from .views import doc_test

from django.conf.urls import url
from . import views

urlpatterns = [
    url('', doc_test)
]
