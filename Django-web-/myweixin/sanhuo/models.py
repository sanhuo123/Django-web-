from __future__ import unicode_literals
# encoding:utf-8
from django.db import models

# Create your models here.
class weixin(models.Model):
    flag=models.IntegerField(null=True)
    uid=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    contenthe = models.TextField(null=True)
    contentme = models.TextField(null=True)