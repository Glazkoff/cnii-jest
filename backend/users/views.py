from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    # return Response("Email аккаунт активирован!")
    html = '<html><head><link rel = "preconnect" href = "https://fonts.googleapis.com" ><link rel = "preconnect" href = "https://fonts.gstatic.com" crossorigin ><link href = "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel = "stylesheet" ><style> * {font-family: "Roboto", sans-serif} </style></head><body><h1> Email аккаунт активирован!</h1><br><a href = "/"> Вернуться на главную </a></body></html>'
    return HttpResponse(html)
