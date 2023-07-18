from django.shortcuts import render,redirect
from django.views import View
from student.forms import StudentLoginForm,ChangepwdForm
from django.contrib.auth import authenticate, login , logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from student.models import Student
from score.models import Score


def logout(request):
    """
    退出登录
    """
    django_logout(request)	# 清除response的cookie和django_session中记录
    return HttpResponseRedirect('/login')

@login_required
def index(request):
    """
    首页
    """
    student_num = request.session.get('student_num','')    # 获取当前登录学生的学号
    student = Student.objects.get(student_num=student_num) # 根据学号查询学生信息
    scores = student.score_set.all() # 获取该学生的所有分数
    return render(request,'index.html',{'scores':scores})  # 渲染模板

@login_required
def score(request,score_id):
    """
    成绩详情
    """
    try:
        score = Score.objects.get(id=score_id)                   # 根据id获取分数信息
    except:
        return render(request, '404.html', {'errmsg':'数据异常'}) # 跳转至404页面
    return render(request, 'score.html', {'score': score})       # 渲染模板

class StudentLoginView(View):
    """
    学生登录页表单
    """
    def get(self,request):
        """
        显示登录页面
        """
        return render(request,'login.html',{'form':StudentLoginForm()}) # 渲染模板

    def post(self,request):
        """
        提交登录页面表单
        """
        form = StudentLoginForm(request.POST) # 接收Form表单
        # 验证表单
        if form.is_valid():
            student_num = request.POST['student_num'] # 获取学号
            password = request.POST['password']       # 获取密码
            user = authenticate(request, username=student_num, password=password)  # 授权校验
            if user is not None:  # 校验成功，获得返回用户信息
                login(request, user)  # 登录用户，设置登录session
                request.session['uid'] = user.id  # 设置用户名的session
                request.session['username'] = user.student.name  # 设置用户名的session
                request.session['student_num'] = user.student.student_num  # 设置用户名的session
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, '用户名和密码不匹配') # 提示错误信息
        return render(request, 'login.html', {'form': form}) # 渲染模板


@login_required
def changepwd(request):
    if request.method == 'GET':
        form = ChangepwdForm() # 实例化表单类
        return render(request, 'changepwd.html', {'form': form}) # 渲染模板
    else:
        form = ChangepwdForm(request.POST) # 接收Form表单
        # 验证表单
        if form.is_valid():
            username = request.user.username # 获取用户名
            oldpassword = request.POST.get('oldpassword', '') # 获取原始密码
            user = authenticate(username=username, password=oldpassword) # 授权校验
            if user is not None and user.is_active:
                # 保存新密码
                newpassword = request.POST.get('newpassword1', '') # 获取新密码
                user.set_password(newpassword) # 设置新密码
                user.save() # 保存用户信息
            else:
                messages.add_message(request, messages.ERROR, '原始密码错误') # 提示错误消息
                return render(request, 'changepwd.html', {'form': form}) # 渲染模板
        else:
            return render(request, 'changepwd.html', {'form': form}) # 渲染模板

def about(request):
    """
    关于我们
    """
    return render(request,'about.html')  # 渲染模板

def contact(request):
    """
    联系我们
    """
    return render(request,'contact.html')  # 渲染模板