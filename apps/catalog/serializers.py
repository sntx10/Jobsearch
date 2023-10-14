from rest_framework import serializers

from apps.catalog.models import Specialization, SpecializationType, SpecializationSubType, Education, JobExperience, \
    LanguageSkill, Recruiter


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ('name',)


class SpecializationTypeSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer()

    class Meta:
        model = SpecializationType
        fields = ('name', 'specialization')


class SpecializationSubTypeSerializer(serializers.ModelSerializer):
    specialization_type = SpecializationTypeSerializer()

    class Meta:
        model = SpecializationSubType
        fields = ('name', 'specialization_type')


class LanguageSkillSerializer(serializers.ModelSerializer):
    language = serializers.CharField(source='language.language')
    level = serializers.CharField(source='level.name')

    class Meta:
        model = LanguageSkill
        fields = ('language', 'level')


class EducationSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source='specialization.name')
    institute = serializers.CharField(source='institute.name')

    class Meta:
        model = Education
        fields = ('degree', 'year', 'specialization', 'institute')


class JobExperienceSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name')

    class Meta:
        model = JobExperience
        fields = ('company_name', 'start_date', 'end_date', 'current_job', 'description')


class RecruiterSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')

    class Meta:
        model = Recruiter
        fields = '__all__'