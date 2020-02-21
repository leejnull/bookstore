from django.db import models
from utils.conventor import ts_from_dt


class Account(models.Model):
    """用户表"""
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '未知')
    )
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11)
    sex = models.CharField(max_length=32, choices=gender, default='未知')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'sex': self.sex,
        }

    class Meta:
        ordering = ['create_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

