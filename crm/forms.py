from django import forms
from django.core.exceptions import ValidationError
from crm import models
import hashlib
from multiselectfield import MultiSelectFormField


class RegForm(forms.ModelForm):
    re_password = forms.CharField(widget=forms.PasswordInput({'placeholder': 're-password'}))
    department = forms.ModelChoiceField(queryset=models.Department.objects.all(), empty_label="Select your Department")
    print(models.Department.objects.all())

    class Meta:
        model = models.UserProfile
        # 生成所有的字段，也可以用列表，生成指定的字段
        fields = '__all__'
        # 排除的字段
        exclude = ['is_active']
        widgets = {
            'username': forms.EmailInput(attrs={'placeholder': 'Username', 'autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile'}),
            'name': forms.TextInput(attrs={'placeholder': 'Real Name'}),
        }

    # Compare the 2 passwords
    def clean(self):
        # 校验唯一性
        self._validate_unique = True
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            # encrypt the password
            md5 = hashlib.md5()
            if password:
                md5.update(password.encode('utf-8'))
            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data
        else:
            self.add_error('re_password', 'Password does not match')
            raise ValidationError('Password does not match')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, MultiSelectFormField):
                # field.widget.attrs['class'] = 'list-group'
                continue
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        self._validate_unique = True
