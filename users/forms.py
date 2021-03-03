from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RegistrationToken


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    token = forms.CharField(required=True, disabled=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', "token"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm Password"})
        self.fields["token"].widget.attrs.update({"placeholder": "Token"})


class RegistrationTokenForm(forms.ModelForm):
    class Meta:
        model = RegistrationToken
        fields = []

    def __init__(self, *args, **kwargs):
        super(RegistrationTokenForm, self).__init__(*args, **kwargs)
