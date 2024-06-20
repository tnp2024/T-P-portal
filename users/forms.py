


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import authenticate  # Import the authenticate function
from django import forms
from .models import CustomUser, Student,Coordinator,TNPOffice,DriveApplication
class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'user_type']  # Include required fields directly

    def __init__(self, *args, view_name=None, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'  # Customize email label

        if view_name == 'register_student':
            self.fields['user_type'].widget = forms.HiddenInput()
                    # ... other field customizations for user_type if needed ...
    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        # Perform any additional validation if needed
        return user_type            
                  


class StudentForm(forms.ModelForm):
    DOB = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    GENDER = forms.ChoiceField(
        choices=Student.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Live_backlogs = forms.ChoiceField(
        choices=Student.Boolean_choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Dead_backlogs = forms.ChoiceField(
        choices=Student.Boolean_choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Year_gap = forms.ChoiceField(
        choices=Student.Gap,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Preference_1 = forms.ChoiceField(
        choices=Student.preferences,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Preference_2 = forms.ChoiceField(
        choices=Student.preferences,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    Preference_3 = forms.ChoiceField(
        choices=Student.preferences,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    # Placed = forms.ChoiceField(
    #     choices=Student.Boolean_choices,
    #     widget=forms.Select(attrs={'class': 'form-select'})
    # )
    # Placement_type = forms.ChoiceField(
    #     choices=Student.Placement_choice,
    #     widget=forms.Select(attrs={'class': 'form-select'})
    # )
    Pass_out_Year = forms.ChoiceField(
        choices=Student.YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'AVG_TILL_SEM_cgpa', 'AVG_TILL_SEM_percentage','Company_name','Placement_type','Placed']

        widgets = {
            'FIRST_NAME': forms.TextInput(attrs={'class': 'form-control'}),
            'MIDDLE_NAME': forms.TextInput(attrs={'class': 'form-control'}),
            'LAST_NAME': forms.TextInput(attrs={'class': 'form-control'}),
            'PRN': forms.NumberInput(attrs={'class': 'form-control'}),
            'EMAIL': forms.EmailInput(attrs={'class': 'form-control'}),
            'PERSONAL_EMAIL': forms.EmailInput(attrs={'class': 'form-control'}),
            'AGE': forms.NumberInput(attrs={'class': 'form-control'}),
            'MOBILE_NO': forms.NumberInput(attrs={'class': 'form-control'}),
            'ALT_Mobile_NO': forms.NumberInput(attrs={'class': 'form-control'}),
            'LOCAL_ADDRS': forms.TextInput(attrs={'class': 'form-control'}),
            'PERM_ADDRS': forms.TextInput(attrs={'class': 'form-control'}),
            'Native_Place': forms.TextInput(attrs={'class': 'form-control'}),
            'X_Percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'X_year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),
            'X_board': forms.TextInput(attrs={'class': 'form-control'}),
            'XII_Percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'XII_year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),
            'XII_board': forms.TextInput(attrs={'class': 'form-control'}),
            'Diploma_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'Diploma_year_of_passing': forms.NumberInput(attrs={'class': 'form-control'}),
            'Diploma_college': forms.TextInput(attrs={'class': 'form-control'}),
            'Diploma_branch': forms.TextInput(attrs={'class': 'form-control'}),
            'Admission_Type': forms.TextInput(attrs={'class': 'form-control'}),
            'SEM_1_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'SEM_2_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'SEM_3_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'SEM_4_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'SEM_5_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'SEM_6_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'SEM_7_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'SEM_8_sgpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'Languages': forms.TextInput(attrs={'class': 'form-control'}),
            'minor_projects': forms.TextInput(attrs={'class': 'form-control'}),
            'major_projects': forms.TextInput(attrs={'class': 'form-control'}),
            'Profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CoordinatorForm(forms.ModelForm):
   class Meta:
         model =Coordinator
         fields = '__all__'
         exclude = ['user']

class TNPOfficeForm(forms.ModelForm):
  class Meta:
        model = TNPOffice
        fields = '__all__'  # Include all fields by default
        exclude = ['user']  

from django.contrib.auth import authenticate

class LoginForm(forms.Form):
  email = forms.EmailField(max_length=254)
  password = forms.CharField(widget=forms.PasswordInput)

  def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')
    password = cleaned_data.get('password')
    user = authenticate(email=email, password=password)
    if not user:
      raise forms.ValidationError('Invalid email or password')
    return cleaned_data
  
class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['Profile_photo', 'PERSONAL_EMAIL', 'MOBILE_NO', 'ALT_Mobile_NO', 'LOCAL_ADDRS', 'PERM_ADDRS', 'Pass_out_Year',
                  'SEM_5_sgpa',  'SEM_6_sgpa',  'SEM_7_sgpa', 
                  'SEM_8_sgpa', 'Live_backlogs', 'Dead_backlogs', 'Year_gap', 'Languages',
                  'minor_projects', 'major_projects', 'Preference_1', 'Preference_2', 'Preference_3', 'Placed']


 
class RoundDataForm(forms.ModelForm):
    class Meta:
        model = DriveApplication
        fields = []  # No fields from the DriveApplication model by default

    selected_students = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    round1 = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)
    round2 = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)
    round3 = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)
    round4 = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)
    round5 = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_students'].queryset = Student.objects.all()  # Assuming Student is the related model

class UploadFilesForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [ 'Xth_marksheet','XIIth_marksheet','Diploma_Firstyear_marksheet','Diploma_Secondyear_marksheet','Diploma_Thirdyear_marksheet','sem1_marksheet','sem2_marksheet','sem3_marksheet','sem4_marksheet','sem5_marksheet',  'sem6_marksheet',  'sem7_marksheet',
                   'sem8_marksheet']
 
from django import forms
from django.contrib.auth.forms import SetPasswordForm

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()




