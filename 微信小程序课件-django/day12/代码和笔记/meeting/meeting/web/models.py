from django.db import models


class UserInfo(models.Model):
    name = models.CharField(verbose_name='用户姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)


class MeetingRoom(models.Model):
    title = models.CharField(verbose_name='会议室', max_length=32)


class Booking(models.Model):
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')

    room = models.ForeignKey(verbose_name='会议室', to='MeetingRoom')

    booking_date = models.DateField(verbose_name='预定日期')

    time_choices = (
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )
    booking_time = models.IntegerField(verbose_name='预定时间段', choices=time_choices)

    class Meta:
        unique_together = (
            ('booking_date', 'booking_time', 'room')
        )


