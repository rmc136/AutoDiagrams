from django import forms

class YAMLUploadForm(forms.Form):
    yaml_file = forms.FileField()