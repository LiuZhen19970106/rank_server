from django.db import models


# Create your models here.

class UserInfo(models.Model):
    client_nums = models.CharField(default="", max_length=100, verbose_name="客户端号", help_text="客户端号")
    score = models.IntegerField(default="", verbose_name="分数", help_text="分数")
