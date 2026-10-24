from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions
from .permissons import IsAdminOrReadOnly
from .serializers import RoomSerializer, OccupiedDateSerializer, UserSerializer
from .models import Room, OccupiedDate, User
from rest_framework.authtoken.models import Token
# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'rooms': reverse('room-list',request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'occupied-dates': reverse('occupieddate-list', request=request, format=format)
    })



class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]



class OccupiedDateList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def ger_queryset(self):
        user = self.request.user
        if not user.is_superuser and not user.is_staff:
            return OccupiedDate.objects.filter(user=user)
        return super().get_queryset()



class OccupiedDateDetail(generics.RetrieveUpdateDestroyAPIView):
     queryset = OccupiedDate.objects.all()
     serializer_class = OccupiedDateSerializer
     permission_classes = [IsAdminOrReadOnly]



class UserList(generics.ListAPIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer

     def get_queryset(self):
         user = self.request.user
         if user.is_staff or user.is_superuser:
             return User.objects.all()
         else:
            return User.objects.filter(id=user.id)



class UserDetail(generics.RetrieveAPIView):
     queryset = User.objects.all()
     serializer_class = UserSerializer

     def get_object(self):
         user = self.request.user
         obj = super().get_object()

         if obj == user or user.is_staff or user.is_superuser:
                return obj
         else:
              raise permissions.PermissionDeni
         


class Register(generics.CreateAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer

        def perform_create(self, serializer):
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=user)

            self.response_data = {
                 "user":{
                      "id": user.id,
                      "username": user.email,
                      "email": user.email,
                      "full_name": user.full_name,
                 },
                 "token": token.key
            }
        
        def create(self, request, *args, **kwrgs):
             super().create(request, *args, **kwrgs)
             return Response(self.response_data)

   
        
class Login(APIView):
     def post(self,reqest,*args,**kwargs):
          username = reqest.data.get("username")
          password = reqest.data.get("password")

          user = authenticate(username=username,password=password)

          if user is None:
               raise AuthenticationFailed('Invalid username or password')
          
          token,created = Token.objects.get_or_create(user=user)

          return Response({
                 "user":{
                      "id": user.id,
                      "username": user.email,
                      "email": user.email,
                      "full_name": user.full_name,
                 },
                 "token": token.key
            })
     
     class TestToken(generics.RetrieveAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer