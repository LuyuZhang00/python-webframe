from django.db import models


class Rsa(models.Model):
    """ 秘钥 """
    status_choices = (
        (1, '启用'),
        (2, '停用'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices)
    user = models.CharField(verbose_name='用户', max_length=32, default='root')
    private_key = models.TextField(verbose_name='私钥')


class Server(models.Model):
    """ 主机表
    例如：公司所有的主机信息
    """
    hostname = models.CharField(verbose_name='主机名', max_length=32)

    def __str__(self):
        return self.hostname


class Project(models.Model):
    """ 项目 """
    title = models.CharField(verbose_name='项目名', max_length=32)
    repo = models.CharField(verbose_name='git仓库地址', max_length=128)  # ['http', 'https', 'ftp', 'ftps']

    def __str__(self):
        return self.title


class ProjectEnv(models.Model):
    """ 项目环境 """
    project = models.ForeignKey(verbose_name='项目', to='Project')
    env_choices = (
        ('test', '测试'),
        ('prod', '正式')
    )
    env = models.CharField(verbose_name='环境', choices=env_choices, max_length=32)
    path = models.CharField(verbose_name='线上部署路径', max_length=128)
    servers = models.ManyToManyField(verbose_name='服务器', to='Server')

    def __str__(self):
        return "%s（%s）" % (self.project.title, self.get_env_display())


class DeployTask(models.Model):
    summary = models.CharField(verbose_name='描述', max_length=64)

    uid = models.CharField(verbose_name='任务ID', max_length=64, help_text="任务ID格式为：项目-版本-时间，例如 cmdb-v1-201911012359.zip")
    status_choices = (
        (1, '待发布'),
        (2, '发布中'),
        (3, '成功'),
        (4, '失败'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    env = models.ForeignKey(verbose_name='环境', to='ProjectEnv')

    # 正式发布用tag
    tag = models.CharField(verbose_name='版本', max_length=32, null=True, blank=True)

    # 测试发布用branch 、commit
    branch = models.CharField(verbose_name='分支', max_length=32, null=True, blank=True)
    commit = models.CharField(verbose_name='提交记录', max_length=40, null=True, blank=True)

    deploy_type_choices = (
        (1, '全量主机发布'),
        (2, '自定义主机发布'),
    )
    deploy_type = models.PositiveSmallIntegerField(verbose_name='发布类型', choices=deploy_type_choices, default=1)

    # 查询
    """
    xx = models.ManyToManyField(verbose_name='自定义主机',
                                to='Server',
                                through='DeployServer',
                                through_fields=('deploy', 'server'))
    """

    before_download_script = models.TextField(verbose_name='下载前脚本', null=True, blank=True)
    after_download_script = models.TextField(verbose_name='下载后脚本', null=True, blank=True)

    before_deploy_script = models.TextField(verbose_name='发布前脚本', null=True, blank=True)
    after_deploy_script = models.TextField(verbose_name='发布后脚本', null=True, blank=True)


class HookScript(models.Model):
    """
    钩子脚本
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    hook_type_choices = (
        (2, '下载前'),
        (4, '下载后'),
        (7, '发布前'),
        (9, '发布后'),
    )
    hook_type = models.IntegerField(verbose_name='钩子类型', choices=hook_type_choices)
    script = models.TextField(verbose_name='脚本内容')


class DeployServer(models.Model):
    """
    上线记录
    """
    deploy = models.ForeignKey(verbose_name='发布任务', to='DeployTask')
    server = models.ForeignKey(verbose_name='服务器', to='Server')
    status_choices = (
        (1, '待发布'),
        (2, '发布中'),
        (3, '成功'),
        (4, '失败'),
    )
    status = models.PositiveSmallIntegerField(verbose_name='状态', choices=status_choices, default=1)


class Diagram(models.Model):
    """发布图标"""
    task = models.ForeignKey(verbose_name='发布任务', to='DeployTask')
    text = models.CharField(verbose_name='文本', max_length=32)
    status_choices = (
        ('gray', '待执行'),
        ('green', '成功'),
        ('red', '失败'),
    )
    status = models.CharField(verbose_name='状态', max_length=32, choices=status_choices, default='gray')
    parent = models.ForeignKey(verbose_name='父节点', to='self', null=True, blank=True)
    deploy_record = models.ForeignKey(verbose_name='服务器发布记录', to='DeployServer', null=True, blank=True)
    log = models.TextField(verbose_name='日志', null=True, blank=True)
