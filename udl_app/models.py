from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    aadhaar_id = models.BigIntegerField(blank=False, unique=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('', kwargs={'username': self.user.username})

    class Meta:
        ordering = ['user']
