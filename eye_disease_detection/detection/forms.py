from django import forms
from .models import Detection

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Detection
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
                'id': 'imageInput'
            })
        }