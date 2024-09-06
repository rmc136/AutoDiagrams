from django import forms
from django.core.validators import FileExtensionValidator

class YAMLUploadForm(forms.Form):
    yaml_file = forms.FileField(
        label='Upload File',
        validators=[FileExtensionValidator(allowed_extensions=['yaml', 'yml', 'json', 'xml'])],
    )
    