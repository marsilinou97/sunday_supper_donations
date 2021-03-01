from django import forms



class RawDataForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    donation_date = forms.DateField(required=False)


    class Meta:


        fields = ['first_name', 'last_name', 'donation_date']

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
        self.fields["donation_date"].widget.attrs.update({"placeholder": "YYYY-MM-DD"})




