from django import forms
from .models import Drive,Activity,Booklets



class DriveForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    application_last_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Drive
        fields = '__all__'

        widgets = {
            'department': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(DriveForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            field.widget.attrs['class'] = 'form-control'
            if name == 'date':
                field.widget.attrs['placeholder'] = 'YYYY-MM-DD'


        
class ActivityForm(forms.ModelForm):
    activity_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Activity
        fields = '__all__'  # You can specify specific fields if needed

        widgets = {
            'department': forms.CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            field.widget.attrs['class'] = 'form-control'
            if name == 'activity_date':
                field.widget.attrs['placeholder'] = 'YYYY-MM-DD'

class BookletForm(forms.ModelForm):
    class Meta:
        model = Booklets
        fields = ['booklet', 'department', 'company_name']                