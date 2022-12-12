# Generated by Django 4.0.5 on 2022-06-16 18:19

import CategoriesAndSizes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(null=True, upload_to=CategoriesAndSizes.models.user_directory_path)),
                ('original_name', models.CharField(blank=True, max_length=150, verbose_name='Nombre original')),
            ],
        ),
        migrations.CreateModel(
            name='SizeCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('categories', models.ManyToManyField(to='CategoriesAndSizes.sizecategory')),
            ],
        ),
    ]
