from django.forms import ModelForm
from django import forms
from rbac.models import Role
class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['title']

        widgets = {
            'title': forms.widgets.Input(attrs={"class": 'form-control'})
        }