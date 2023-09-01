from django import forms
from .models import UserProperty
from django.utils import formats

class UserPropertyForm(forms.ModelForm):
    username = forms.CharField(max_length=12, label='用户名', required=False, widget=forms.TextInput(attrs={'rows': 1, 'placeholder': '[默认为原名]'}))

    class Meta:
        model = UserProperty
        fields = ['birthday', 'introduce', 'sex']
        labels = {'birthday': '生日', 'introduce': '简介', 'sex': '性别'}
        widgets = {
            'birthday': forms.DateInput(attrs={'type':'date'})
        }