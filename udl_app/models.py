from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    aadhaar_id = models.BigIntegerField(blank=False, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)  # type: ignore

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['user']
