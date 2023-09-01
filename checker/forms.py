from django import forms
from blogs.models import BlogPostMedia

class ActiveForm(forms.Form):
    activate = forms.BooleanField(label='active', required=False)