from django.contrib import admin

from apps.catalog.models import Specialization, SpecializationType, SpecializationSubType, CompanyIndustry, \
    CompanyIndustryType, CompanyIndustrySubType, Language, LanguageLevel, LanguageSkill, Company, Skill, \
    Education, Institute, NativeLanguage, JobExperience, Recruiter
from apps.product.models import Resume, Vacancy

# Register your models here.

admin.site.register(Resume)
admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(Specialization)
admin.site.register(SpecializationType)
admin.site.register(SpecializationSubType)
admin.site.register(CompanyIndustry)
admin.site.register(CompanyIndustryType)
admin.site.register(CompanyIndustrySubType)
admin.site.register(Language)
admin.site.register(LanguageLevel)
admin.site.register(LanguageSkill)
admin.site.register(Skill)
admin.site.register(JobExperience)
admin.site.register(Education)
admin.site.register(Institute)
admin.site.register(NativeLanguage)
admin.site.register(Recruiter)