from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import customer_profile

# Create your views here.


class Login(APIView):
    @staticmethod
    def get(request):
        b = customer_profile(user_name="Yax", password="YAX", email="yaxb@gmail.com", address="kkkkk")
        b.save()
        return Response("HELLO W OR LD")