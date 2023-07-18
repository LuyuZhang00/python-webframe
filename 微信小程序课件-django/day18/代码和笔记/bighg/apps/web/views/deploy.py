import os
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .. import models
from ..forms.deploy_task import DeployTaskModelForm

from utils.repository import GitRepository
from utils.response import BaseResponse


def deploy_task_list(request, env_id):
    """
    server列表
    :param request: 请求相关所有数据
    :param env_id: 环境ID
    :return: 页面
    """
    env_object = models.ProjectEnv.objects.filter(id=env_id).first()
    queryset = models.DeployTask.objects.filter(env=env_object).order_by('-id')
    return render(request, 'web/deploy_task_list.html', {'queryset': queryset, 'env_object': env_object})


def deploy_task_add(request, env_id):
    env_object = models.ProjectEnv.objects.filter(id=env_id).first()
    if request.method == "GET":
        form = DeployTaskModelForm(env_object)
        return render(request, 'web/deploy_task_form.html', {'form': form, "env_id": env_id, 'env_object': env_object})

    form = DeployTaskModelForm(env_object, data=request.POST)
    if form.is_valid():
        form.save(is_create=True)
        return redirect(reverse('deploy_task_list', kwargs={'env_id': env_id}))
    return render(request, 'web/deploy_task_form.html', {'form': form, "env_id": env_id, 'env_object': env_object})


def deploy_task_del(request, pk):
    models.DeployTask.objects.filter(pk=pk).delete()
    return JsonResponse({'status': True})


def git_commits(request):
    """
    根据分支获取所有的commit
    :param request:
    :return:
    """
    response = BaseResponse()
    try:
        env_id = request.GET.get('env_id')
        branch = request.GET.get('branch')

        env_object = models.ProjectEnv.objects.filter(id=env_id).first()
        url = env_object.project.repo
        project_name = env_object.project.title
        local_path = os.path.join(settings.HG_DEPLOY_BASE_PATH, project_name)
        repo_object = GitRepository(local_path, url)

        # 切换到指定分支
        repo_object.change_to_branch(branch)
        # 获取所有提交记录
        commit_list = repo_object.commits()
        response.data = commit_list
    except Exception as e:
        response.status = False
        response.error = '版本获取失败'
    return JsonResponse(response.dict)


def get_script_template(request, template_id):
    """
    获取脚本模板
    :param request:
    :param template_id:
    :return:
    """
    response = BaseResponse()
    try:
        script_object = models.HookScript.objects.filter(id=template_id).first()
        response.data = script_object.script
    except Exception:
        response.status = False
        response.error = '获取模板失败'
    return JsonResponse(response.dict)


def channels_deploy(request, task_id):
    """
    websocket发布
    :param request:
    :param task_id:
    :return:
    """
    task_object = models.DeployTask.objects.filter(id=task_id).first()

    deploy_server_list = models.DeployServer.objects.filter(deploy=task_object)
    return render(request, 'web/channels_deploy.html',
                  {'deploy_server_list': deploy_server_list, 'task_id': task_id, 'task_object': task_object})
