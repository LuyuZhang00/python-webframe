from django.db import models
from utils.base_models import CreateUpdateMixin
from student.models import Student


class Score(CreateUpdateMixin):
    title = models.CharField(max_length=20,help_text='title/考试名称',verbose_name='考试名称')
    score = models.DecimalField(max_digits=5,decimal_places=2,help_text='score/分数',verbose_name='分数')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,verbose_name='学生姓名')  # 设置外键

    def student_name(self):
        """
        获取学生姓名
        """
        self.verbose_name = '学生姓名'
        return self.student.name
    student_name.short_description = '学生姓名'

    def student_num(self):
        """
        获取学号
        """
        self.verbose_name = '学号'
        return self.student.student_num
    student_num.short_description = '学号'

    class Meta:
        db_table = "score"
        verbose_name_plural = "成绩信息"
        verbose_name = "成绩信息"
