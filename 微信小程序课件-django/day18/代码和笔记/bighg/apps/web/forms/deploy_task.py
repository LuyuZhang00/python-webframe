import os
import datetime
from django import forms
from django.forms.widgets import Select
from django.conf import settings
from .. import models
from .bootstrap import BootStrapModelForm
from utils.repository import GitRepository


class DeployTaskModelForm(BootStrapModelForm):
    hook_list = [
        {'key': 'before_download', 'nid': 2},
        {'key': 'after_download', 'nid': 4},
        {'key': 'before_deploy', 'nid': 7},
        {'key': 'after_deploy', 'nid': 9},
    ]
    exclude_bootstrap_fields = [
        'before_download_template',
        'after_download_template',
        'before_deploy_template',
        'after_deploy_template'
    ]

    deploy_servers = forms.MultipleChoiceField(label='选择主机', required=False)

    before_download_select = forms.ChoiceField(required=False, label='下载前')
    before_download_title = forms.CharField(required=False, label='模板名称')
    before_download_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    after_download_select = forms.ChoiceField(required=False, label='下载后')
    after_download_title = forms.CharField(required=False, label='模板名称')
    after_download_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    before_deploy_select = forms.ChoiceField(required=False, label='发布前')
    before_deploy_title = forms.CharField(required=False, label='模板名称')
    before_deploy_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    after_deploy_select = forms.ChoiceField(required=False, label='下载后')
    after_deploy_title = forms.CharField(required=False, label='模板名称')
    after_deploy_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    class Meta:
        model = models.DeployTask
        exclude = ['uid', 'status', 'env', 'xx']

        widgets = {
            'tag': Select(choices=[]),
            'branch': Select(choices=[]),
            'commit': Select(choices=[]),
        }

    def __init__(self, env_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env_object = env_object
        self.init_git(env_object)
        self.init_hook()

        self.fields['deploy_servers'].choices = env_object.servers.all().values_list('id', 'hostname')
        if self.instance:
            init_server_id_list = models.DeployServer.objects.filter(deploy=self.instance).values_list('server_id')
            self.fields['deploy_servers'].initial = [item[0] for item in init_server_id_list]

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = "请输入" + field.label

    def init_hook(self):
        before_download_select = [(None, '请选择模板'), ]
        before_download_select += models.HookScript.objects.filter(hook_type=2).values_list('id', 'title')
        self.fields['before_download_select'].choices = before_download_select

        after_download_select = [(None, '请选择模板'), ]
        after_download_select += models.HookScript.objects.filter(hook_type=4).values_list('id', 'title')
        self.fields['after_download_select'].choices = after_download_select

        before_deploy_select = [(None, '请选择模板'), ]
        before_deploy_select += models.HookScript.objects.filter(hook_type=7).values_list('id', 'title')
        self.fields['before_deploy_select'].choices = before_deploy_select

        after_deploy_select = [(None, '请选择模板'), ]
        after_deploy_select += models.HookScript.objects.filter(hook_type=9).values_list('id', 'title')
        self.fields['after_deploy_select'].choices = after_deploy_select

    def init_git(self, env_object):
        """
        初始化git信息，以便动态显示版本、分支
        :param env_object:
        :return:
        """
        url = env_object.project.repo
        project_name = env_object.project.title
        local_path = os.path.join(settings.HG_DEPLOY_BASE_PATH, project_name, project_name)
        repo_object = GitRepository(local_path, url)

        repo_object.pull()

        tag_choices = [(None, '请选择分支'), ]
        tag_choices = tag_choices + [(item, item) for item in repo_object.tags()]
        self.fields['tag'].widget.choices = tag_choices

        branch_choices = [(None, '请选择分支'), ]
        branch_choices = branch_choices + [(item, item) for item in repo_object.branches()]
        self.fields['branch'].widget.choices = branch_choices

        commit_choices = [(None, '请选择提交记录'), ]
        self.fields['commit'].widget.choices = commit_choices

    def clean(self):

        # 处理版本
        deploy_type = self.cleaned_data.get('deploy_type')
        deploy_servers = self.cleaned_data.get('deploy_servers')
        if deploy_type == 1:
            # 全量发布
            # 如果有选择服务，则视为无效，自己去获取 self.env_object.servers.all()
            if deploy_servers:
                self.add_error('deploy_servers', '全量上线无需选择服务器')
        elif deploy_type == 2:
            # 自定义发布
            # 读取用户选择的deploy_servers，用户必须选择
            if not deploy_servers:
                self.add_error('deploy_servers', '自定义上线请选择服务器')
        else:
            self.add_error('deploy_type', '发布类型错误')

        tag = self.cleaned_data.get('tag')
        branch = self.cleaned_data.get('branch')
        commit = self.cleaned_data.get('commit')
        if tag:
            if branch:
                self.add_error('branch', '基于Tag发布，请移除分支选项')
            if commit:
                self.add_error('commit', '基于Tag发布，请移除提交记录选项')

        else:
            if not branch:
                self.add_error('branch', '必须选择分支')
            if not commit:
                self.add_error('commit', '必须选择提交记录')

        # 处理钩子，如果已选择保存为模板，则title不能为空。

        for row in self.hook_list:
            is_template = self.cleaned_data.get(row['key'] + '_template')
            if not is_template:
                continue
            title_key = row['key'] + '_title'
            title = self.cleaned_data.get(title_key)
            if not title:
                self.add_error(title_key, '保存为模板时，必须输入模板名称')

            script_key = row['key'] + '_script'
            script = self.cleaned_data.get(script_key)
            if not script:
                self.add_error(script_key, '保存为模板时，必须输入脚本内容')

        # 整体错误信息
        # self.add_error(None,'tag或branch任选其一')  # form.non_field_errors.0
        # raise ValidationError('tag或branch任选其一') # form.non_field_errors.0
        return self.cleaned_data

    def save(self, is_create=False, commit=True):
        """
        将当前发布任务保存到数据库
        :param commit:
        :return:
        """
        if is_create:
            self.instance.status = 1
            self.instance.env = self.env_object
            self.instance.uid = self.create_uid()
        self.instance.save()

        deploy_type = self.cleaned_data.get('deploy_type')
        if deploy_type == 1:
            queryset = self.env_object.servers.all()
            deploy_server_id_list = [item.id for item in queryset]
        else:
            deploy_server_id_list = self.cleaned_data['deploy_servers']
        task_id = self.instance.id

        # 如果是更新，则先删除所有，再重新创建一遍
        if not is_create:
            models.DeployServer.objects.filter(deploy_id=task_id).delete()

        object_list = []
        for server_id in deploy_server_id_list:
            object_list.append(models.DeployServer(deploy_id=task_id, server_id=server_id))
        if object_list:
            models.DeployServer.objects.bulk_create(object_list)

        hook_object_list = []
        for row in self.hook_list:
            is_template = self.cleaned_data.get(row['key'] + '_template')
            if is_template:
                hook_object_list.append(models.HookScript(hook_type=row['nid'],
                                                          title=self.cleaned_data.get(row['key'] + '_title'),
                                                          script=self.cleaned_data.get(row['key'] + '_script')))
        if hook_object_list:
            models.HookScript.objects.bulk_create(hook_object_list)

        project_name = self.env_object.project.title
        local_path = os.path.join(
            settings.HG_DEPLOY_BASE_PATH,
            project_name,
            self.env_object.env,
            self.instance.uid,
            project_name
        )
        GitRepository(local_path, self.env_object.project.repo)

    def create_uid(self):
        project_name = self.env_object.project.title
        version = self.cleaned_data.get('tag')
        if not version:
            version = "%s-%s" % (self.cleaned_data['branch'], self.cleaned_data['commit'])
        date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return "%s-%s-%s" % (project_name, version, date)
