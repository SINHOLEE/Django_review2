from django.db import models
from django.contrib.auth.models import AbstractUser  # user model을 customize하기 위해 상속할 수 있는 메소드를 임포트한다. 
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='followings'
        )
