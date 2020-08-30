from django.contrib.auth.forms import AuthenticationForm

from authapp.models import ShopClient


class ShopLoginForm(AuthenticationForm):
    class Meta:
        model = ShopClient
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
