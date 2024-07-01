


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

    Pass_out_Year = forms.ChoiceField(
        choices=Student.YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'AVG_TILL_SEM_cgpa', 'AVG_TILL_SEM_percentage','Company_name','Placement_type','Placed']
        widgets = {
            'FIRST_NAME': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'MIDDLE_NAME': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your middle name'}),
            'LAST_NAME': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'PRN': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your PRN'}),
            'EMAIL': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email (same as Email address field)'}),
            'PERSONAL_EMAIL': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your personal email'}),
            'AGE': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'MOBILE_NO': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
            'ALT_Mobile_NO': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your alternate mobile number'}),
            'LOCAL_ADDRS': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your local address'}),
            'PERM_ADDRS': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your permanent address'}),
            'Native_Place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your native place'}),
            'X_Percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 10th percentage'}),
            'X_year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 10th year of passing'}),
            'X_board': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 10th board'}),
            'XII_Percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 12th percentage'}),
            'XII_year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 12th year of passing'}),
            'XII_board': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 12th board'}),
            'Diploma_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your diploma percentage'}),
            'Diploma_year_of_passing': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your diploma year of passing'}),
            'Diploma_college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your diploma college'}),
            'Diploma_branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your diploma branch'}),
            'Admission_Type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your admission type'}),
            'SEM_1_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 1 SGPA'}),
            'SEM_2_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 2 SGPA'}),
            'SEM_3_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 3 SGPA'}),
            'SEM_4_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 4 SGPA'}),
            'SEM_5_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 5 SGPA'}),
            'SEM_6_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 6 SGPA'}),
            'SEM_7_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 7 SGPA'}),
            'SEM_8_sgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your SEM 8 SGPA'}),
            'Languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter programming languages you know'}),
            'minor_projects': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your minor projects'}),
            'major_projects': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your major projects'}),
            'Profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload your profile photo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'user_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your user type'}),
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
        fields = [ 'PERSONAL_EMAIL', 'MOBILE_NO', 'ALT_Mobile_NO', 'LOCAL_ADDRS', 'PERM_ADDRS', 'Pass_out_Year',
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
        fields = [ 'Profile_photo','Xth_marksheet','XIIth_marksheet','Diploma_Firstyear_marksheet','Diploma_Secondyear_marksheet','Diploma_Thirdyear_marksheet','sem1_marksheet','sem2_marksheet','sem3_marksheet','sem4_marksheet','sem5_marksheet',  'sem6_marksheet',  'sem7_marksheet',
                   'sem8_marksheet']
 




