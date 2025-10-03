from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get' , 'put'])
    def me(self, request):
        user = User.objects.get(id=request.user.id)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# accounts/views.py
from rest_framework import generics
from .serializers import RegisterSerializer
# from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()  # Access the through model for the ManyToMany relationship
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TeamCreateUpdateSerializer
        return TeamSerializer

