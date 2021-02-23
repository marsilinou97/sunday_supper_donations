from datetime import datetime

from django import forms

from .models import *


class DonorInformationForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    dob = forms.DateField(required=False,
                          widget=forms.DateInput(attrs={'type': 'date', "min": "1900-01-01",
                                                        "max": datetime.today().strftime('%Y-%m-%d')}))
    address1 = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zip = forms.CharField(required=False)

    class Meta:
        # model = input
        fields = ['first_name', 'last_name', 'dob', 'address1', 'address2', 'city', 'state', 'zip', 'email']

    def __init__(self, *args, **kwargs):
        super(DonorInformationForm, self).__init__(*args, **kwargs)

        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["first_name"].widget.attrs.update({"placeholder": "First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Last Name"})
        self.fields["dob"].widget.attrs.update({"placeholder": "D.O.B"})
        self.fields["address1"].widget.attrs.update({"placeholder": "Address Line 1"})
        self.fields["address2"].widget.attrs.update({"placeholder": "Address Line 2"})
        self.fields["city"].widget.attrs.update({"placeholder": "City"})
        self.fields["state"].widget.attrs.update({"placeholder": "State"})
        self.fields["zip"].widget.attrs.update({"placeholder": "Zip Code"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})


class DonationForm(forms.ModelForm):
    date_received = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    thanks_sent = forms.BooleanField(required=False)
    comment = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={'rows': 5}
        ),
        help_text="Comment",
    )

    class Meta:
        model = Donation
        fields = ['date_received', 'thanks_sent', 'comment']

    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)

        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["thanks_sent"].widget.attrs.update({"class": "form-check-input"})
        self.fields["comment"].widget.attrs.update({"placeholder": "Comment"})

    def clean(self):
        cleaned_data = super(DonationForm, self).clean()
        return cleaned_data


class ItemForm(forms.Form):
    type = forms.ChoiceField(required=False)
    quantity = forms.IntegerField(required=False)

    class Meta:
        # model = input
        fields = ['type', 'quantity', 'name']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["type"].widget.attrs.update({"placeholder": "type"})
        self.fields["quantity"].widget.attrs.update({"placeholder": "0"})


class FundsForm(forms.Form):
    type = forms.ChoiceField(required=False)
    amount = forms.DecimalField(required=False)

    class Meta:
        # model = input
        fields = ['type', 'amount']

    def __init__(self, *args, **kwargs):
        super(FundsForm, self).__init__(*args, **kwargs)

        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'
