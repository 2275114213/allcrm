from django import forms
from app01.models import Customer
class CustomerModelForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):
                field.widget.attrs.update({'class':'form-control'})