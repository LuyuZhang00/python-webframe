"""
关于rsa相关所有操作
"""

from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .. import models
from ..forms.server import ServerModelForm

def server_list(request):
    """
    server列表
    :param request: 请求相关所有数据
    :return: 页面
    """
    queryset = models.Server.objects.all()
    return render(request,'web/server_list.html',{'queryset':queryset})

def server_add(request):
    """ 添加 """
    if request.method == "GET":
        form = ServerModelForm()
        return render(request,'web/form.html',{'form':form})

    form = ServerModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('server_list')

    return render(request, 'web/form.html', {'form': form})

def server_edit(request,pk):
    """ 编辑 """
    query_object = models.Server.objects.filter(pk=pk).first()
    if not query_object:
        return HttpResponse('ID不存在')

    if request.method == "GET":
        form = ServerModelForm(instance=query_object)
        return render(request,'web/form.html',{'form':form})

    form = ServerModelForm(data=request.POST,instance=query_object)
    if form.is_valid():
        form.save()
        return redirect('server_list')

    return render(request, 'web/form.html', {'form': form})


def server_del(request,pk):
    """ 删除 """
    models.Server.objects.filter(pk=pk).delete()
    return JsonResponse({'status':True})