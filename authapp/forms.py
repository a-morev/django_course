import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import django.forms as df

from authapp.models import ShopClient, ShopClientProfile


class ShopLoginForm(AuthenticationForm):
    class Meta:
        model = ShopClient
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopRegistrationForm(UserCreationForm):
    class Meta:
        model = ShopClient
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        years_old = self.cleaned_data['age']
        if years_old < 14:
            raise df.ValidationError('Попробуйте зарегистрироваться, когда будете старше!')
        return years_old

    def save(self, commit=True):
        user = super().save(commit)

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopProfileForm(UserChangeForm):
    class Meta:
        model = ShopClient
        fields = ('username', 'first_name', 'email', 'password', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = df.HiddenInput()

    def clean_age(self):
        years_old = self.cleaned_data['age']
        if years_old < 14:
            raise df.ValidationError('Попробуйте зарегистрироваться, когда будете старше!')
        return years_old


class ShopClientProfileEditForm(df.ModelForm):
    class Meta:
        model = ShopClientProfile
        fields = ('tagline', 'aboutMe', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
