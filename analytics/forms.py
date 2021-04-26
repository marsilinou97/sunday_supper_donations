from django import forms
from helpers import remove_html_tags


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

    donation_year = forms.CharField(max_length=4, required=False)

    class Meta:
        fields = ['first_name', 'last_name', 'donation_year']

    def __init__(self, *args, **kwargs):
        super(ChartsForm, self).__init__(*args, **kwargs)

        self.fields["donation_year"].widget.attrs.update({"placeholder": "YYYY"})


    def clean(self):
        cleaned_data = super(ChartsForm, self).clean()
        cleaned_data = remove_html_tags(cleaned_data)
        return cleaned_data
