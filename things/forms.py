from django.forms import ModelForm
from .models import Things

class ThingsForm(ModelForm):
    class Meta:
        model = Things
        fields = ['title', 'memo', 'important']
