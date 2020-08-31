from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import django.forms as df

from authapp.models import ShopClient


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
