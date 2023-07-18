#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.forms import ModelForm


class BootStrapModelForm(ModelForm):
    exclude_bootstrap_class = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name in self.exclude_bootstrap_class:
                continue
            old_class = field.widget.attrs.get('class', "")
            field.widget.attrs['class'] = old_class + ' form-control'
