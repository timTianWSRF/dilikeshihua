from django.db import models


# Create your models here.
class WangUser(models.Model):
    username = models.CharField(max_length=32, unique=True)  #  用户名
    password = models.CharField(max_length=32)  # 密码
    # email = models.CharField(max_length=32)   # 邮箱
