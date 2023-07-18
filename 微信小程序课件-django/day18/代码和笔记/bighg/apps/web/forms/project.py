from django import forms
from .. import models
from .bootstrap import BootStrapModelForm


class ProjectModelForm(BootStrapModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"


class ProjectEnvModelForm(BootStrapModelForm):
    class Meta:
        model = models.ProjectEnv
        fields = "__all__"
