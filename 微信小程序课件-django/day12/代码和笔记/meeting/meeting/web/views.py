import json
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from . import models
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.db.models import Q
from django.db.utils import IntegrityError


class LoginForm(Form):
    name = fields.CharField(
        required=True,
        error_messages={'required': '用户名不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名', 'id': 'name'})
    )
    password = fields.CharField(
        required=True,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码', 'id': 'password'})
    )
    rmb = fields.BooleanField(required=False, widget=widgets.CheckboxInput(attrs={'value': 1}))


def md5(val):
    import hashlib
    m = hashlib.md5()
    m.update(val.encode('utf-8'))
    return m.hexdigest()


def auth(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/login/')
        return func(request, *args, **kwargs)

    return inner


def auth_json(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return JsonResponse({'status': False, 'msg': '用户未登录'})
        return func(request, *args, **kwargs)

    return inner


def login(request):
    """
    用户登录
    """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            rmb = form.cleaned_data.pop('rmb')
            form.cleaned_data['password'] = md5(form.cleaned_data['password'])
            user = models.UserInfo.objects.filter(**form.cleaned_data).first()
            if user:
                request.session['user_info'] = {'id': user.id, 'name': user.name}
                if rmb:
                    request.session.set_expiry(60 * 60 * 24 * 30)
                return redirect('/index/')
            else:
                form.add_error('password', '密码错误')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})


@auth
def index(request):
    """
    会议室预定首页
    :param request: 
    :return: 
    """
    time_choices = models.Booking.time_choices
    return render(request, 'index.html', {'time_choices': time_choices})


@auth_json
def booking(request):
    """
    获取会议室预定情况以及预定会议室
    :param request: 
    :param date: 
    :return: 
    """
    ret = {'code': 1000, 'msg': None, 'data': None}
    current_date = datetime.datetime.now().date()

    if request.method == "GET":
        try:
            fetch_date = request.GET.get('date')
            fetch_date = datetime.datetime.strptime(fetch_date, '%Y-%m-%d').date()
            if fetch_date < current_date:
                raise Exception('查询时间不能是以前的时间')

            booking_list = models.Booking.objects.filter(booking_date=fetch_date).select_related('user',
                                                                                                 'room').order_by(
                'booking_time')

            booking_dict = {}
            for item in booking_list:
                if item.room_id not in booking_dict:
                    booking_dict[item.room_id] = {item.booking_time: {'name': item.user.name, 'id': item.user.id}}
                else:
                    if item.booking_time not in booking_dict[item.room_id]:
                        booking_dict[item.room_id][item.booking_time] = {'name': item.user.name, 'id': item.user.id}
            """
            {
                room_id:{
                    time_id:{''},
                    time_id:{''},
                    time_id:{''},
                }
            }
            """

            room_list = models.MeetingRoom.objects.all()

            booking_info = []
            for room in room_list:
                temp = [{'text': room.title, 'attrs': {'rid': room.id}, 'chosen': False}]
                for choice in models.Booking.time_choices:
                    v = {'text': '', 'attrs': {'time-id': choice[0], 'room-id': room.id}, 'chosen': False}
                    if room.id in booking_dict and choice[0] in booking_dict[room.id]:
                        v['text'] = booking_dict[room.id][choice[0]]['name']
                        v['chosen'] = True
                        if booking_dict[room.id][choice[0]]['id'] != request.session['user_info']['id']:
                            v['attrs']['disable'] = 'true'
                    temp.append(v)
                booking_info.append(temp)

            ret['data'] = booking_info
        except Exception as e:
            ret['code'] = 1001
            ret['msg'] = str(e)
        return JsonResponse(ret)
    else:
        try:
            booking_date = request.POST.get('date')
            booking_date = datetime.datetime.strptime(booking_date, '%Y-%m-%d').date()
            if booking_date < current_date:
                raise Exception('查询时间不能是以前的时间')

            booking_info = json.loads(request.POST.get('data'))

            for room_id, time_id_list in booking_info['add'].items():
                if room_id not in booking_info['del']:
                    continue
                for time_id in list(time_id_list):
                    if time_id in booking_info['del'][room_id]:
                        booking_info['del'][room_id].remove(time_id)
                        booking_info['add'][room_id].remove(time_id)

            add_booking_list = []
            for room_id, time_id_list in booking_info['add'].items():
                for time_id in time_id_list:
                    obj = models.Booking(
                        user_id=request.session['user_info']['id'],
                        room_id=room_id,
                        booking_time=time_id,
                        booking_date=booking_date
                    )
                    add_booking_list.append(obj)
            models.Booking.objects.bulk_create(add_booking_list)

            remove_booking = Q()
            for room_id, time_id_list in booking_info['del'].items():
                for time_id in time_id_list:
                    temp = Q()
                    temp.connector = 'AND'
                    temp.children.append(('user_id', request.session['user_info']['id'],))
                    temp.children.append(('booking_date', booking_date,))
                    temp.children.append(('room_id', room_id,))
                    temp.children.append(('booking_time', time_id,))
                    remove_booking.add(temp, 'OR')
            if remove_booking:
                models.Booking.objects.filter(remove_booking).delete()
        except IntegrityError as e:
            ret['code'] = 1011
            ret['msg'] = '会议室已被预定'

        except Exception as e:
            ret['code'] = 1012
            ret['msg'] = '预定失败：%s' % str(e)

    return JsonResponse(ret)
