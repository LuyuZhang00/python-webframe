from django import forms
from django.contrib.auth.models import User

class StudentLoginForm(forms.Form):
    student_num = forms.CharField(
        label='学号',
        required=True,
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-0',
            'placeholder': "请输入学号"
        }),
        error_messages={
            'required': '学号不能为空',
            'max_length': '长度不能超过50个字符',
        }
    )
    password = forms.CharField(
        label='密码',
        required=True,
        min_length = 6,
        max_length = 50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-0',
            'placeholder':"请输入密码"
        }),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '长度不能少于6个字符',
            'max_length': '长度不能超过50个字符',
        }
    )

    # 二次验证函数的名字是固定写法，以clear_开头，后面跟上字段的变量名
    def clean_student_num(self):
        # 通过了validators的验证之后，在进行二次验证
        student_num = self.cleaned_data['student_num']
        try:
            user = User.objects.get(username=student_num)  # 使用student_num获取Django用户
        except User.DoesNotExist:
            raise forms.ValidationError('学号不存在', 'invalid')
        else:
            return student_num


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        label="原密码",
        required=True,
        min_length=6,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-0',
                'placeholder':"原密码",
            }
        ),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '长度不能少于6个字符',
            'max_length': '长度不能超过50个字符',
        }
    )
    newpassword1 = forms.CharField(
        label="新密码",
        required=True,
        min_length=6,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-0',
                'placeholder':"新密码",
            }
        ),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '长度不能少于6个字符',
            'max_length': '长度不能超过50个字符',
        }
    )
    newpassword2 = forms.CharField(
        label="确认密码",
        required=True,
        min_length=6,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-0',
                'placeholder':u"确认密码",
            }
        ),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '长度不能少于6个字符',
            'max_length': '长度不能超过50个字符',
        }
     )
    def clean_newpassword2(self):
        if not self.is_valid():
            raise forms.ValidationError("所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError("两次输入的新密码不一致")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data