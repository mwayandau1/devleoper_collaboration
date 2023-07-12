from django.db import models
import uuid
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedIn = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created  = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)


    def __str__(self):
        return str(self.username)
    


class Skills(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created  = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)


    class Meta:
        verbose_name = 'skills'
        verbose_name_plural = 'skills'

    def __str__(self):
        return str(self.name)
