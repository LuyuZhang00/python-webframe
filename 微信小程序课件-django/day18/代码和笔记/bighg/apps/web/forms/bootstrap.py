from django import forms


class BootStrapModelForm(forms.ModelForm):
    exclude_bootstrap_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.exclude_bootstrap_fields:
                continue
            cls = field.widget.attrs.get('class')
            if cls:
                field.widget.attrs['class'] = cls + " form-control"
            else:
                field.widget.attrs['class'] = 'form-control'
