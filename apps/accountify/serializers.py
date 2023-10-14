from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accountify.tasks import send_confirmation_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=5, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email(user.email, code)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=5, write_only=True)
    new_password = serializers.CharField(required=True, min_length=5, write_only=True)
    new_password_repeat = serializers.CharField(required=True, min_length=5, write_only=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно')
        return old_password

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_repeat']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=5, write_only=True)
