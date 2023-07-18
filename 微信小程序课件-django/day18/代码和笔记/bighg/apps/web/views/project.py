"""
关于rsa相关所有操作
"""

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .. import models
from ..forms.project import ProjectModelForm, ProjectEnvModelForm


def project_list(request):
    """
    server列表
    :param request: 请求相关所有数据
    :return: 页面
    """
    queryset = models.Project.objects.all()
    return render(request, 'web/project_list.html', {'queryset': queryset})


def project_add(request):
    """ 添加 """
    if request.method == "GET":
        form = ProjectModelForm()
        return render(request, 'web/form.html', {'form': form})

    form = ProjectModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('project_list')

    return render(request, 'web/form.html', {'form': form})


def project_edit(request, pk):
    """ 编辑 """
    query_object = models.Project.objects.filter(pk=pk).first()
    if not query_object:
        return HttpResponse('ID不存在')

    if request.method == "GET":
        form = ProjectModelForm(instance=query_object)
        return render(request, 'web/form.html', {'form': form})

    form = ProjectModelForm(data=request.POST, instance=query_object)
    if form.is_valid():
        form.save()
        return redirect('project_list')

    return render(request, 'web/form.html', {'form': form})


def project_del(request, pk):
    """ 删除 """
    models.Project.objects.filter(pk=pk).delete()
    return JsonResponse({'status': True})


def project_env_list(request):
    """
    server列表
    :param request: 请求相关所有数据
    :return: 页面
    """
    queryset = models.ProjectEnv.objects.all()
    return render(request, 'web/project_env_list.html', {'queryset': queryset})


def project_env_add(request):
    """ 添加 """
    if request.method == "GET":
        form = ProjectEnvModelForm()
        return render(request, 'web/form.html', {'form': form})

    form = ProjectEnvModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('project_env_list')

    return render(request, 'web/form.html', {'form': form})


def project_env_edit(request, pk):
    """ 编辑 """
    query_object = models.ProjectEnv.objects.filter(pk=pk).first()
    if not query_object:
        return HttpResponse('ID不存在')

    if request.method == "GET":
        form = ProjectEnvModelForm(instance=query_object)
        return render(request, 'web/form.html', {'form': form})

    form = ProjectEnvModelForm(data=request.POST, instance=query_object)
    if form.is_valid():
        form.save()
        return redirect('project_env_list')

    return render(request, 'web/form.html', {'form': form})


def project_env_del(request, pk):
    """ 删除 """
    models.ProjectEnv.objects.filter(pk=pk).delete()
    return JsonResponse({'status': True})
