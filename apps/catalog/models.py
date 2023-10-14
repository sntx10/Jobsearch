from django.contrib.auth import get_user_model
from django.db import models

from location_field.models.plain import PlainLocationField

# from apps.product.models import Vacancy
User = get_user_model()


class Specialization(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    keywords = models.TextField()

    def __str__(self):
        return self.name


class SpecializationType(models.Model):
    name = models.CharField(max_length=128)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='sp_types')
    description = models.TextField()
    keywords = models.TextField()

    def __str__(self):
        return f'{self.name} ({self.specialization.name})'


class SpecializationSubType(models.Model):
    name = models.CharField(max_length=128)
    specialization_type = models.ForeignKey(SpecializationType, on_delete=models.CASCADE, related_name='sps_type')
    description = models.TextField()
    keywords = models.TextField()

    def __str__(self):
        return f'{self.name}: {self.specialization_type.name} ({self.specialization_type.specialization.name})'


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_users')
    name = models.CharField(max_length=255)
    specialization = models.ForeignKey(SpecializationSubType, on_delete=models.CASCADE,
                                       related_name='company_specializations')
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyIndustry(models.Model):
    name = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='industries')

    def __str__(self):
        return self.name


class CompanyIndustryType(models.Model):
    name = models.CharField(max_length=128)
    industry = models.ForeignKey(CompanyIndustry, on_delete=models.CASCADE, related_name='types')

    def __str__(self):
        return f'{self.name}: {self.industry.name}'


class CompanyIndustrySubType(models.Model):
    name = models.CharField(max_length=128)
    industry_type = models.ForeignKey(CompanyIndustryType, on_delete=models.CASCADE, related_name='subtypes')

    def __str__(self):
        return f'{self.name}: {self.industry_type.name} ({self.industry_type.industry.name})'


class Skill(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


LVL = (
    ('kg', 'Кыргызский'),
    ('ru', 'Русский'),
    ('en', 'Английский'),
    ('fr', 'Французский'),
    ('de', 'Немецкий'),
    ('es', 'Испанский'),
    ('it', 'Итальянский'),
    ('pt', 'Португальский'),
    ('pl', 'Польский'),
    ('uk', 'Украинский'),
    ('tr', 'Турецкий'),
    ('zh', 'Китайский'),
    ('ja', 'Японский'),
    ('ko', 'Корейский'),
    ('ar', 'Арабский'),
    ('he', 'Иврит'),
    ('hi', 'Хинди'),
    ('ur', 'Урду')
)


class NativeLanguage(models.Model):
    language = models.CharField(choices=LVL, max_length=2)

    def __str__(self):
        return self.language


class Language(models.Model):
    language = models.CharField(choices=LVL, max_length=2)

    def __str__(self):
        return self.language


class LanguageLevel(models.Model):
    LVL = (
        ('A1', 'A1 -- Начальный'),
        ('A2', 'A2 -- Элементарный'),
        ('B1', 'B1 -- Средний'),
        ('B2', 'B2 -- Средне-продвинутый'),
        ('C1', 'C1 -- Продвинутый'),
        ('C2', 'C2 -- В совершестве')
    )

    name = models.CharField(choices=LVL, max_length=128)

    def __str__(self):
        return self.name


class LanguageSkill(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='skills')
    level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.language}: {self.level}'


class JobExperience(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_positions')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current_job = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.company}: {self.description}"


class Institute(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10)
    established_year = models.IntegerField()

    def __str__(self):
        return self.name


class Education(models.Model):
    degree = models.CharField(max_length=255)
    year = models.IntegerField()
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE,
                                       related_name='education_specialization')
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='institutes')

    def __str__(self):
        return self.degree


class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recruiter_users')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recruiter_companies')
    can_create_vacancy = models.BooleanField(default=False)