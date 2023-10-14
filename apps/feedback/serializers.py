from rest_framework import serializers

from apps.feedback.models import Favorite, UnwantedVacancy, UnwantedCompany, Subscription, Review


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        rep['vacancy'] = instance.vacancy.title
        return rep



class UnwantedSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnwantedVacancy
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.first_name
        rep['vacancy'] = instance.vacancy.title


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['company'] = instance.company.name
        return rep


class CompanyUnwantedSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnwantedCompany
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['company'] = instance.company.name
        return rep


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name')
    rating = serializers.IntegerField(min_value=1, max_value=5)
    vacancy = serializers.CharField(required=False)
    text = serializers.CharField(required=True)

    class Meta:
        model = Review
        fields = ['rating', 'vacancy', 'text', 'user']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['vacancy'] = instance.vacancy.title
        return rep