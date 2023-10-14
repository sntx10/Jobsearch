from rest_framework import serializers

from apps.userprofile.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile
        fields = '__all__'
