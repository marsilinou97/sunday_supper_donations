from django import forms
from helpers import remove_html_tags
from datetime import date

# Generate range of years for year dropdown. Default value set to current calendar year.
current_year = date.today().year

YEAR_CHOICES = [(current_year, current_year)]

for year in range(2015, current_year + 21):
    YEAR_CHOICES.append((year, year))



class RawDataForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    donation_date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    donation_date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        fields = ['first_name', 'last_name', 'donation_date_from', 'donation_date_to']

    def __init__(self, *args, **kwargs):
        super(RawDataForm, self).__init__(*args, **kwargs)

        '''
        Removed to keep form widgets on single line
        
        fields = self.visible_fields()
        for visible in fields:
            # Add class to each of the form elements
            visible.field.widget.attrs['class'] = 'form-control'
        '''

        self.fields["first_name"].widget.attrs.update({"placeholder": "First Name"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Last Name"})
        self.fields["donation_date_from"].widget.attrs.update({"placeholder": "YYYY-MM-DD"})
        self.fields["donation_date_to"].widget.attrs.update({"placeholder": "YYYY-MM-DD"})

    def clean(self):
        cleaned_data = super(RawDataForm, self).clean()
        cleaned_data = remove_html_tags(cleaned_data)
        return cleaned_data



class ChartsForm(forms.Form):

    donation_year = forms.ChoiceField(label="Donation Year", choices=YEAR_CHOICES)

    class Meta:
        fields = ['donation_year']

    def __init__(self, *args, **kwargs):
        super(ChartsForm, self).__init__(*args, **kwargs)

        self.fields["donation_year"].widget.attrs.update({"class": "form-control-md"})
        self.fields["donation_year"].widget.attrs.update({"id": "year-dropdown"})


    def clean(self):
        cleaned_data = super(ChartsForm, self).clean()
        cleaned_data = remove_html_tags(cleaned_data)
        return cleaned_data
