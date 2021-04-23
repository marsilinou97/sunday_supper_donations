from django import forms
from helpers import remove_html_tags
from settings.queries import get_all_roles

BOOLEAN_VALUES = [(True,"True"),(False,"False")]
class TokenForm(forms.Form):
    id = forms.CharField(max_length=50,required=False)
    token = forms.CharField(max_length=50,required=False)
    date_created = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    creator_name = forms.CharField(max_length=50,required=False)
    active = forms.ChoiceField(required=False, choices=BOOLEAN_VALUES)
    expiration_period = forms.CharField(max_length=50,required=False)

    class Meta:
        fields = ['id', 'token', 'date_created', 'creator_name', 'active', 'expiration_period']

    def __init__(self, *args, **kwargs):
        super(TokenForm, self).__init__(*args, **kwargs)

        self.fields["id"].widget.attrs.update({"placeholder": "id"})
        self.fields["token"].widget.attrs.update({"placeholder": "token"})
        self.fields["date_created"].widget.attrs.update({"placeholder": "YYYY-MM-DD"})
        self.fields["creator_name"].widget.attrs.update({"placeholder": "creator"})
        self.fields["active"].widget.attrs.update({"placeholder": "None"})
        self.fields["expiration_period"].widget.attrs.update({"placeholder": "-1"})

    def clean(self):
        cleaned_data = super(TokenForm, self).clean()
        cleaned_data = remove_html_tags(cleaned_data)
        return cleaned_data

class UserRoleForm(forms.Form):
    id = forms.CharField(max_length=50,required=False)
    username = forms.CharField(max_length=50,required=False)
    email = forms.EmailField(required=False)
    active = forms.ChoiceField(required=False, choices=BOOLEAN_VALUES)

    available_roles = list(get_all_roles())
    for i in range(len(available_roles)):
        available_roles[i] = (available_roles[i]['role'],
                                available_roles[i]['role'])
    role = forms.ChoiceField(required=False, choices=available_roles)

    class Meta:
        fields = ['id', 'username', 'email', 'active', 'role']

    def __init__(self, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)

        self.fields["id"].widget.attrs.update({"placeholder": "id"})
        self.fields["username"].widget.attrs.update({"placeholder": "username"})
        self.fields["email"].widget.attrs.update({"placeholder": "email"})
        self.fields["active"].widget.attrs.update({"placeholder": "None"})
        self.fields["role"].widget.attrs.update({"placeholder": "None"})

    def clean(self):
        cleaned_data = super(TokenForm, self).clean()
        cleaned_data = remove_html_tags(cleaned_data)
        return cleaned_data
