from django.db import models
from django.contrib.auth.models import User



class Data(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    login = models.TextField()
    password = models.TextField()
