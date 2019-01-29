from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=False, null=False)
    text = models.TextField(blank=False, null=True)
    created = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    users_likes = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #TODO for additional user params, for example link to avatar