from datetime import datetime
from django import forms
from .models import *
from helpers import remove_html_tags


class DonorInformationForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    address1 = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zip = forms.CharField(required=False)

    class Meta:
        model = Donor
        fields = ['first_name', 'last_name', 'phone_number', 'address1', 'address2', 'city', 'state', 'zip', 'email']

    def __init__(self, *args, **kwargs):
        super(DonorInformationForm, self).__init__(*args, **kwargs)

        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["first_name"].widget.attrs.update({"placeholder": "First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Last Name"})
        self.fields["phone_number"].widget.attrs.update({"placeholder": "Phone Number"})
        self.fields["address1"].widget.attrs.update({"placeholder": "Address Line 1"})
        self.fields["address2"].widget.attrs.update({"placeholder": "Address Line 2"})
        self.fields["city"].widget.attrs.update({"placeholder": "City"})
        self.fields["state"].widget.attrs.update({"placeholder": "State"})
        self.fields["zip"].widget.attrs.update({"placeholder": "Zip Code"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})

US_STATES = [('',''), ('al', 'Alabama'), ('ak', 'Alaska'), ('as', 'American Samoa'), ('az', 'Arizona'), ('ar', 'Arkansas'),
             ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('de', 'Delaware'), ('dc', 'District of Columbia'),
             ('fl', 'Florida'), ('ga', 'Georgia'), ('gu', 'Guam'), ('hi', 'Hawaii'), ('id', 'Idaho'), ('il', 'Illinois'),
             ('in', 'Indiana'), ('ia', 'Iowa'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('me', 'Maine'),
             ('md', 'Maryland'), ('ma', 'Massachusetts'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('ms', 'Mississippi'),
             ('mo', 'Missouri'), ('mt', 'Montana'), ('ne', 'Nebraska'), ('nv', 'Nevada'), ('nh', 'New Hampshire'),
             ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('ny', 'New York'), ('nc', 'North Carolina'), ('nd', 'North Dakota'),
             ('mp', 'Northern Mariana Islands'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'),
             ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'),
             ('tx', 'Texas'), ('ut', 'Utah'), ('vt', 'Vermont'), ('vi', 'Virgin Islands'), ('va', 'Virginia'), ('wa', 'Washington'),
             ('wv', 'West Virginia'), ('wi', 'Wisconsin'), ('wy', 'Wyoming')]

class DonorEditForm(forms.ModelForm):
    id = forms.CharField(required=False, max_length=6)
    first_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=False, max_length=50)
    email = forms.EmailField(required=False, max_length=50)
    phone_number = forms.CharField(required=False, max_length=20)
    address1 = forms.CharField(required=False, max_length=50)
    address2 = forms.CharField(required=False, max_length=50)
    city = forms.CharField(required=False, max_length=50)
    state = forms.ChoiceField(required=False, choices=US_STATES)
    zip = forms.CharField(required=False, max_length=5)

    class Meta:
        model = Donor
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'address1', 'address2', 'city', 'state', 'zip', 'email']

    def __init__(self, *args, **kwargs):
        super(DonorEditForm, self).__init__(*args, **kwargs)
        fields = self.visible_fields()
        for visible in fields:
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["id"].widget.attrs.update({"placeholder": "id"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Last Name"})
        self.fields["phone_number"].widget.attrs.update({"placeholder": "Phone Number"})
        self.fields["address1"].widget.attrs.update({"placeholder": "Address Line 1"})
        self.fields["address2"].widget.attrs.update({"placeholder": "Address Line 2"})
        self.fields["city"].widget.attrs.update({"placeholder": "City"})
        self.fields["state"].widget.attrs.update({"placeholder": "None"})
        self.fields["zip"].widget.attrs.update({"placeholder": "Zip Code"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})

    def clean(self):
        cleaned_data = super(DonorEditForm, self).clean()
        cleaned_data = remove_html_tags(cleaned_data)
        return cleaned_data

class DonationForm(forms.Form):
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
        cleaned_data = remove_html_tags(cleaned_data)
        return cleaned_data


class ItemForm(forms.Form):

    #TODO: Make models that holds the choices defined here
    item_choices = (
        ("1","Gift Cards"),
        ("2","Food"),
        ("3","Clothing"),
        ("4","Misc.")
    )

    DONATION_TYPES = [
                  ('giftcard', 'Gift Cards'),
                  ('clothing', 'Clothing'),
                  ('food', 'Food'),
                  ('misc', 'Miscellaneous')
                  ]

    clothing_types = [
        ('men','Men'),
        ('women','Women'),
        ('children','Children')
    ]

    business = [
        ("Trader Joe's","Trader Joe's"),
        ('tar','Target'),
        ('bestbuy','BestBuy')
    ]

    type = forms.ChoiceField(required=False, choices=DONATION_TYPES)
    quantity = forms.IntegerField(required=False)
    sub_type_name = forms.CharField(required=False)
    sub_type_clothing = forms.ChoiceField(required=False, choices=clothing_types)
    sub_type_business = forms.ChoiceField(required=False, choices=business)
    amount = forms.DecimalField(required=False)


    class Meta:
        # model = input
        fields = ['type', 'quantity', 'sub_type_name','sub_type_clothing','sub_type_business', 'amount']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields["type"].widget.attrs.update({"placeholder": "Type"})
        self.fields["quantity"].widget.attrs.update({"placeholder": "0"})
        self.fields["sub_type_name"].widget.attrs.update({"placeholder": "Name"})
        self.fields["sub_type_clothing"].widget.attrs.update({"placeholder": "Type"})
        self.fields["sub_type_business"].widget.attrs.update({"placeholder": "Business"})
        self.fields["amount"].widget.attrs.update({"placeholder": "0"})


class FundsForm(forms.Form):

    amount = forms.DecimalField(required=False)
    fund_types = [
        (None,"N/A"),
        ('Cash', 'Cash'),
        ('Check', 'Check'),
        ('Electronic', 'Electronic')
    ]

    type = forms.ChoiceField(required=False, choices=fund_types)

    class Meta:
        # model = input
        fields = ['type', 'amount']

    def __init__(self, *args, **kwargs):
        super(FundsForm, self).__init__(*args, **kwargs)

        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'
