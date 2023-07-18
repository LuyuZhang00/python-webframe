from django import forms
from .. import models
from .bootstrap import BootStrapModelForm


class RsaModelForm(BootStrapModelForm):
    class Meta:
        model = models.Rsa
        fields = "__all__"

