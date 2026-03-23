from rest_framework import generics
from people.serializers import UserSerializer
from django.contrib.auth.models import User


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class UserRetrieve(generics.RetrieveAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer