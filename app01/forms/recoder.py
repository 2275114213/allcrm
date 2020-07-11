from django import forms
from app01.models import ConsultRecord
class RecoderCustomerFrom(forms.ModelForm):
    class Meta:
        model = ConsultRecord
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):
                field.widget.attrs.update({'class':'form-control'})
