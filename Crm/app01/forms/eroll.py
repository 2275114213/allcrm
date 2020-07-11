from django import forms
from app01.models import Enrollment
class ErollmentForm(forms.ModelForm):
    class Meta:
        model=Enrollment
        exclude=['delete_status']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in  self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})