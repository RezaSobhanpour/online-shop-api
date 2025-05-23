from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import User
from .serializers import UserSerializer, UserChangePasswordSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return User.objects.all()
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.request.user.is_superuser:
            return [IsAdminUser()]
        if self.request.user.is_authenticated:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if self.request.user == instance or self.request.user.is_superuser:
            return instance.delete()
        raise PermissionDenied('you can only delete your own account!')

    def perform_update(self, serializer):
        if self.request.user == self.get_object() or self.request.user.is_superuser:
            return serializer.save()
        raise PermissionDenied('you can only update your own account!')

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated],
            serializer_class=UserChangePasswordSerializer)
    def set_password(self):
        new_password = self.request.data.get('new_password')
        confirm_password = self.request.data.get('confirm_password')
        user = self.request.user

        if not new_password or new_password != confirm_password:
            return Response({'messages': 'new password does not match or missing'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'messages': 'password seccesfully changes'})
