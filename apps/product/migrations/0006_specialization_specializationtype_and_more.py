# Generated by Django 4.2 on 2023-04-28 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_resume_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SpecializationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sp_types', to='product.specialization')),
            ],
        ),
        migrations.CreateModel(
            name='SpecializationSubType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
                ('specialization_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sps_type', to='product.specializationtype')),
            ],
        ),
    ]
