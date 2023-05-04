from django import forms
from django.core.validators import FileExtensionValidator


class UploadDocumentForm(forms.Form):
    url = forms.URLField(required=False, label='File link  ')
    language = forms.CharField(max_length=10, required=False, label='Language  ')
    file = forms.FileField(required=False, label='File upload   ', validators=[FileExtensionValidator(
        allowed_extensions=['xml', 'yml'])])



