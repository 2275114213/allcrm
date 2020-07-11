from django import forms
from app01.models import *

from django.forms import widgets as wid
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
import re
class UserModelForm(forms.ModelForm):
    r_pwd = forms.CharField(error_messages={'r_pwd':"不能为空"}, label='确认密码',
                            widget=wid.PasswordInput(attrs={"class": "form-control"}))
    # r_pwd = forms.CharField(label='确认密码',error_messages={'r_pwd':"不能为空"})
    # widgets={'r_pwd':wid.PasswordInput(attrs={'type':"password"})}
    class Meta:
        model=UserInfo
        fields=['username','email','gender','tel',"password"]
        # fields = "__all__"
        labels={'username':"用户名",'password':'密码','email':'邮箱',"tel":"电话",'gender':"性别"}
        help_texts={'username':'请输入用户名',"password":'请输入密码',"email":'请输入163邮箱','tel':'请输入电话号码'}
        widgets={'password':wid.PasswordInput(attrs={'placeholder':'请输入由数字与字母组成的长度不小于5密码'}),'username':wid.TextInput(attrs={'placeholder':'请输入不少于五位的用户名'}),'email':wid.EmailInput(attrs={'placeholder':'请输入163邮箱'}),'tel':wid.TextInput(attrs={'placeholder':'请输入手机号'})}

        #如果有时间限制格式:
            # widgets={'pub_date':wid.TextInput(attrs={'type':'date'})}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            print(filed.error_messages)
            filed.error_messages={"required":"不能为空","invalid": "格式错误"}
            filed.widget.attrs.update({'class': 'form-control'})
    #
    def clean_tel(self):
        tel=self.cleaned_data.get('tel')
        if tel:
            if re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$',tel):
                return tel
        else:
            raise ValidationError("手机号码非法")
    def clean_email(self):
        import re
        email = self.cleaned_data.get('email')
        if re.search('[0-9a-zA-Z]+@163\.com', email):
            return email
        else:
            if email=='':
                raise  ValidationError('邮箱不能为空')
            else:
                raise ValidationError('请输入163.com邮箱')
    def clean_username(self):
        username=self.cleaned_data.get('username')
        ret = UserInfo.objects.filter(username=username)
        if ret:
            raise ValidationError('用户名已存在')
        else:
            return username

    def clean(self):
        password =  self.cleaned_data.get('password')
        r_pwd= self.cleaned_data.get('r_pwd')
        print(password,r_pwd)

        if password==r_pwd:
            print('haha')
            return self.cleaned_data
        else:
            self.add_error('r_pwd',ValidationError('密码不一致'))

    def save(self, commit=True):
        # Save the provided password in hashed format
        # 继承基类的save()
        user = super(UserModelForm, self).save(commit=False)
        # 把明文密码改成密文
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user