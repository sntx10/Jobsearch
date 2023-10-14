# Generated by Django 4.2 on 2023-05-03 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_education_specialization'),
        ('product', '0017_resume_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='necessary_skills',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='required_experience',
            field=models.CharField(choices=[('no_experience', 'Без опыта'), ('less_than_1_year', 'Менее 1 года'), ('1_3_years', '1-3 года'), ('3_6_years', '3-6 лет'), ('more_than_6_years', 'Более 6 лет')], default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vacancy',
            name='responsibilities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.skill'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='what_do_we_offer',
            field=models.CharField(default=11, max_length=512),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='knowledge_of_languages',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='knowledge_of_languages',
            field=models.ManyToManyField(blank=True, to='catalog.language'),
        ),
    ]