from rest_framework import serializers
from .models import User
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    is_superuser = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'password2', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError('passwords do not match')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        is_superuser = validated_data.pop('is_superuser')
        if is_superuser:
            user = User.objects.create_superuser(password=password, **validated_data)
        else:
            user = User.objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)

        is_superuser = validated_data.pop('is_superuser', None)

        if is_superuser:
            instance.is_superuser = True
            instance.is_staff = True

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError('old password is not correct')
        return value

    def validate_new_password(self, value):
        user = self.context.get('request').user
        password_validation.validate_password(value, user)
        if user.check_password(value):
            raise serializers.ValidationError('new password and the old password are the same!')

        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError('new password does not match')
        return attrs

    def save(self):
        user = self.context.get('request').user
        if not user:
            raise serializers.ValidationError('user does not exist!')
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
