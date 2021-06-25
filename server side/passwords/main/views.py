from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from cryptography.fernet import Fernet
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from .models import Data
from .forms import LoginForm, UserRegisterForm
from .serializers import DataSerializer
from .permissions import IsOwner


class SignUpView(CreateView):
    """Sign up users."""
    template_name = 'main/register.html'
    success_url = reverse_lazy('main:success_view')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"



class SuccessView(TemplateView):
    template_name = 'main/success.html'


class DataList(APIView):
    """List all data, or create a new data."""
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get(self, request, format=None):
        data = self.request.user.data_set.all()
        serializer = DataSerializer(data, many=True)
        password = self.request.headers['password']
        key = settings.ENCRIPTION_KEY + password.encode()
        f = Fernet(key)
        for c in range(len(serializer.data)):
            title = serializer.data[c]['title']
            serializer.data[c]['title'] = f.decrypt(title[2:-1].encode())
            login = serializer.data[c]['login']
            serializer.data[c]['login'] = f.decrypt(login[2:-1].encode())
            password = serializer.data[c]['password']
            serializer.data[c]['password'] = f.decrypt(login[2:-1].encode())
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            password = self.request.headers['password']
            key = settings.ENCRIPTION_KEY + password.encode()
            f = Fernet(key)
            serializer.save(owner = self.request.user,
                            title = f.encrypt(serializer.validated_data['title'].encode()),
                            login = f.encrypt(serializer.validated_data['login'].encode()),
                            password = f.encrypt(serializer.validated_data['password'].encode())
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DataDetail(APIView):
    """
    Retrieve, update or delete a data instance.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_object(self, pk):
        try:
            return Data.objects.get(pk=pk)
        except Data.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        print(data)
        serializer = DataSerializer(data)
        password = self.request.headers['password']
        key = settings.ENCRIPTION_KEY + password.encode()
        f = Fernet(key)
        title = serializer.data['title']
        serializer.data['title'] = f.decrypt(title[2:-1].encode())
        login = serializer.data['login']
        serializer.data['login'] = f.decrypt(login[2:-1].encode())
        password = serializer.data['password']
        serializer.data['password'] = f.decrypt(login[2:-1].encode())

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = DataSerializer(data, data=request.data)
        if serializer.is_valid():
            password = self.request.headers['password']
            key = settings.ENCRIPTION_KEY + password.encode()
            f = Fernet(key)
            serializer.save(owner = self.request.user,
                            title = f.encrypt(serializer.validated_data['title'].encode()),
                            login = f.encrypt(serializer.validated_data['login'].encode()),
                            password = f.encrypt(serializer.validated_data['password'].encode())
                            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
