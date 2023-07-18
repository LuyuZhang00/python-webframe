from django import forms
from .. import models
from .bootstrap import BootStrapModelForm


class ServerModelForm(BootStrapModelForm):
    class Meta:
        model = models.Server
        fields = "__all__"

