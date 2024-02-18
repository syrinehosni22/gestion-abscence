from django.contrib.auth.models import AbstractUser
from django.db import models

from classes.models import Class


class User(AbstractUser):
    ROLES = (
        ('teacher', 'teacher'),
        ('student', 'student'),
        ('admin', 'admin')
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLES, default='student')
    profile_image = models.ImageField(upload_to='profile_images/', blank=False)
    classe = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"


class UserImage(models.Model):
    image = models.ImageField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
