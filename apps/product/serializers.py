from rest_framework import serializers

from apps.catalog.models import Company
from apps.catalog.serializers import LanguageSkillSerializer, EducationSerializer, JobExperienceSerializer, \
    SpecializationSubTypeSerializer
from apps.product.models import Resume, Vacancy


class ResumeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    class Meta:
        model = Resume
        fields = ('user', 'first_name', 'last_name', 'title', 'specialization', 'city', 'location', 'birthday',
                  'phone', 'summary', 'skills', 'place_of_work', 'job_experiences', 'employment', 'schedule',
                  'work_experience', 'native_language', 'knowledge_of_languages', 'is_looking_for_job', 'gender',
                  'salary', 'about_me', 'education', 'created_at', 'updated_at')


class ResumeListSerializer(serializers.ModelSerializer):
    job_experiences = JobExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ('title', 'work_experience', 'job_experiences', 'updated_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.is_looking_for_job is not None:
            ret['is_looking_for_job'] = instance.get_is_looking_for_job_display()
        else:
            del ret['is_looking_for_job']
        return ret


class ResumeDetailSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source='specialization.name')
    skills = serializers.SerializerMethodField()
    knowledge_of_languages = LanguageSkillSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    job_experiences = JobExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = ('gender', 'city', 'birthday', 'title', 'specialization', 'employment', 'schedule', 'work_experience',
                  'skills', 'education', 'knowledge_of_languages', 'job_experiences')

    def get_skills(self, obj):
        return list(obj.skills.values_list('title', flat=True))


class ResumeUpdateSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source='specialization.name')
    skills = serializers.SerializerMethodField()
    knowledge_of_languages = LanguageSkillSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = '__all__'

    def get_skills(self, obj):
        return list(obj.skills.values_list('title', flat=True))


class VacancySerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')

    class Meta:
        model = Vacancy
        fields = ('title', 'company', 'city', 'created_at')


class VacancyDetailSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name')
    skills = serializers.SerializerMethodField()
    knowledge_of_languages = LanguageSkillSerializer(many=True, read_only=True)
    specialization = serializers.CharField(source='specialization.name')

    class Meta:
        model = Vacancy
        fields = ('title', 'company', 'description', 'requirements', 'responsibilities', 'salary',
                  'required_experience', 'contact_information', 'city', 'location', 'employment', 'specialization',
                  'knowledge_of_languages', 'necessary_skills', 'skills', 'what_do_we_offer',
                  'created_at', 'updated_at')

    def get_skills(self, obj):
        return list(obj.skills.values_list('title', flat=True))


class VacancyCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')

    class Meta:
        model = Vacancy
        fields = '__all__'


class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name', 'logo')


class CompanyDetailSerializer(serializers.ModelSerializer):
    specialization = SpecializationSubTypeSerializer()

    class Meta:
        model = Company
        fields = ('name', 'logo', 'description', 'specialization',  'city', 'location', 'website')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


