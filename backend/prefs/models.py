from django.db import models

# Create your models here.
class Pref(models.Model):
    pref_string = models.CharField(max_length=300, unique=True)
    bot_id = models.CharField(max_length=50, unique=True)
    groupchat_url = models.URLField(unique=True)
    groupchat_id = models.CharField(max_length=50, unique=True)
