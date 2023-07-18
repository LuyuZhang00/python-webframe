from django.db import models
from utils.base_models import CreateUpdateMixin
from teacher.models import Teacher
from django.contrib.auth.models import User


class Student(CreateUpdateMixin):
    student_num = models.CharField(max_length=10,unique=True,verbose_name='学号')
    name = models.CharField(max_length=20,help_text='name/姓名',verbose_name='姓名')
    gender = models.CharField(max_length=32, choices=(('male','男'),('female','女')), default='男',help_text='gender/性别',verbose_name='性别')
    phone = models.CharField(max_length=11,help_text='phone/联系电话',verbose_name='联系电话')
    birthday = models.DateField(verbose_name='出生日期')
    # user表一对一关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # teacher表以对多关联
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 设置外键

    def __str__(self):
        return self.name

    def teacher_name(self):
        """
        获取老师名称
        """
        self.verbose_name = '老师名称'
        return self.teacher.name
    teacher_name.short_description = '老师名称'

    def class_name(self):
        """
        获取班级名称
        """
        return self.teacher.class_name
    class_name.short_description = '班级名称'

    class Meta:
        db_table = "student"
        verbose_name_plural = "学生信息"
        verbose_name = "学生信息"




