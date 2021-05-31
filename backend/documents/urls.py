# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.TemplateView.as_view()),
# ]

from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.generate_document, name='generate_document')
]
