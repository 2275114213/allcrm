from django import forms
from app01.models import ClassStudyRecord
class ClassStudyRecordForm(forms.ModelForm):
    class Meta:
        model = ClassStudyRecord
        fields="__all__"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            from django.forms.fields import BooleanField
            if isinstance(field,BooleanField):
                continue
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})