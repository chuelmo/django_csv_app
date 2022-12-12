from django.db import models
import os
import uuid

class SizeCategory(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.description

class Size(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    categories = models.ManyToManyField(SizeCategory)
    
    def __str__(self):
        return self.name


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)

class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to=user_directory_path, null=True)
    original_name = models.CharField(max_length=150, verbose_name='Nombre original', blank=True)

