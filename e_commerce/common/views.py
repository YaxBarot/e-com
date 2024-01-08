from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class Login(APIView):
    @staticmethod
    def get(request):
        print("jj")
        return Response("HELLO W OR LD")