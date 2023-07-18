from django.db import models
from utils.base_models import CreateUpdateMixin
from django.contrib.auth.models import User


class Teacher(CreateUpdateMixin):
    tid = models.IntegerField(primary_key=True,verbose_name='老师ID')
    name = models.CharField(max_length=20,help_text='name/姓名',verbose_name='姓名')
    email = models.CharField(max_length=60, unique=True,help_text='email/邮箱',verbose_name='邮箱')
    class_name = models.CharField(max_length=50,  help_text='class_name/班级名称',verbose_name='班级名称')
    gender = models.CharField(max_length=32, choices=(('male','男'),('female','女')), default='男',help_text='gender/性别',verbose_name='性别')
    phone = models.CharField(max_length=11, unique=True,help_text='phone/手机号',verbose_name='手机号')
    # user表一对一关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    class Meta:
        db_table = "teacher"
        verbose_name_plural = "老师信息"
        verbose_name = "老师信息"


