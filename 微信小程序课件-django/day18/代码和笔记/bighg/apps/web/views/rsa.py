"""
关于rsa相关所有操作
"""

from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .. import models
from ..forms.rsa import RsaModelForm

def rsa_list(request):
    """
    rsa列表
    :param request: 请求相关所有数据
    :return: 页面
    """
    queryset = models.Rsa.objects.all()
    return render(request,'web/rsa_list.html',{'queryset':queryset})

def rsa_add(request):
    """ 添加 """
    if request.method == "GET":
        form = RsaModelForm()
        return render(request,'web/form.html',{'form':form})

    form = RsaModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('rsa_list')

    return render(request, 'web/form.html', {'form': form})

def rsa_edit(request,pk):
    """ 编辑 """
    query_object = models.Rsa.objects.filter(pk=pk).first()
    if not query_object:
        return HttpResponse('ID不存在')

    if request.method == "GET":
        form = RsaModelForm(instance=query_object)
        return render(request,'web/form.html',{'form':form})

    form = RsaModelForm(data=request.POST,instance=query_object)
    if form.is_valid():
        form.save()
        return redirect('rsa_list')

    return render(request, 'web/form.html', {'form': form})


def rsa_del(request,pk):
    """ 删除 """
    models.Rsa.objects.filter(pk=pk).delete()
    return JsonResponse({'status':True})