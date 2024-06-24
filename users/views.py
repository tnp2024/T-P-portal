from .models import Student,Coordinator,TNPOffice,Drive, DriveApplication,Activity,ActivityApplication,CustomUser,ProfileChange
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from .forms import StudentForm,CustomUserForm,CoordinatorForm,TNPOfficeForm,LoginForm,ProfileChangeForm,UploadFilesForm
from django.contrib.auth.decorators import login_required
from notices.views import student_required,coordinator_required,tnpoffice_required,student_not_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render







def search_students(request):
    query = request.GET.get('query')
    students = Student.objects.filter(Q(FIRST_NAME__icontains=query) | Q(PRN__icontains=query)| Q(MIDDLE_NAME__icontains=query)| Q(LAST_NAME__icontains=query))
    return render(request, 'search_results.html', {'students': students, 'query': query})


@login_required
def student_profile(request, student_prn):
    student = get_object_or_404(Student, PRN=student_prn)
    has_pending_requests = ProfileChange.objects.filter(student=student, status='pending').exists()

    if (request.user.user_type == 'Coordinator' or request.user.user_type == 'TNP-Office') \
        or (request.user.student.PRN == student_prn):
        # Allow access to tnpOffice,coordinators and the profile owner

        return render(request, 'studentProfile.html', {'student': student,'has_pending_requests':has_pending_requests})
    else:
        # Redirect or display an error message
        return redirect('all-drives')  # Redirect to the dashboard page, or display an error message

from django.http import HttpResponseBadRequest

def edit_student_profile(request, student_prn):
    student = get_object_or_404(Student, PRN=student_prn)
    
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            # Handle Profile_photo separately
            if 'Profile_photo' in form.changed_data:
                profile_photo = form.cleaned_data['Profile_photo']
                student.Profile_photo = profile_photo
                student.save(update_fields=['Profile_photo'])

            # Get the changed data from the form
            changed_fields = {}
            for field in form.changed_data:
                changed_fields[field] = (form.initial.get(field), form.cleaned_data.get(field))
            
            # Create ProfileChange objects and trigger coordinator
            trigger_coordinator(student, changed_fields)
            # No direct saving of the form here

            return redirect('student_profile', student_prn=student_prn)
        else:
            # Form is not valid, return bad request response
            return HttpResponseBadRequest("Form is not valid. Please check your input.")
    else:
        form = ProfileChangeForm(instance=student)
    
    return render(request, 'edit_student_profile.html', {'form': form, 'student': student})

def trigger_coordinator(student, changed_fields):
    department = student.department
    coordinators = Coordinator.objects.filter(department=department).order_by('id')  # Order coordinators by id

    # Determine which coordinator to assign the request based on PRN
    last_digit = int(str(student.PRN)[-1])  # Get the last digit of PRN

    # Select the coordinator based on the last digit (even or odd)
    if last_digit % 2 == 0:
        coordinator = coordinators.first()  # Assign to the first coordinator
    else:
        coordinator = coordinators.last()   # Assign to the last coordinator

    # Create or update the ProfileChange instance for each changed field
    for field_name, (old_value, new_value) in changed_fields.items():
        # Create ProfileChange instance with the selected coordinator
        profile_change = ProfileChange.objects.create(
            student=student,
            field_changed=field_name,
            old_value=old_value,
            new_value=new_value,
            status="pending",
            coordinator=coordinator
        )

    # Return the selected coordinator (for debugging or further use if needed)
    return coordinator



def profile_changes_for_coordinator(request):
    # Retrieve the currently logged-in coordinator
    coordinator_user = request.user

    # Retrieve the coordinator object associated with the current user
    coordinator = Coordinator.objects.get(user=coordinator_user)

    # Retrieve the department of the coordinator
    coordinator_department = coordinator.department

    # Retrieve all profile changes for this coordinator's department
    all_changes = ProfileChange.objects.filter(
        coordinator__user=coordinator_user,
        coordinator__department=coordinator_department
    ).order_by('-created_at')

    # Count pending changes
    pending_changes_count = all_changes.filter(status='pending').count()

    # Pagination settings
    paginator = Paginator(all_changes, 20)  # 20 items per page
    page_number = request.GET.get('page')

    try:
        all_changes_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_changes_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_changes_page = paginator.page(paginator.num_pages)

    context = {
        'all_changes': all_changes_page,
        'pending_changes_count': pending_changes_count
    }

    return render(request, 'student_profilechange_requests.html', context)



def approve_profile_change(request, change_id):
    profile_change = get_object_or_404(ProfileChange, pk=change_id)
    if profile_change.status in ('approved', 'denied'):
      return redirect('approve_profile_change')
    # Get the student object associated with the profile change
    student = profile_change.student

    # Get the field names and corresponding old and new values from the profile change
    field_changed = profile_change.field_changed
    old_value = profile_change.old_value
    new_value = profile_change.new_value
    
    # Apply changes dynamically based on the field changed
    setattr(student, field_changed, new_value)
    student.save()

    # Update the status of the profile change to 'approved'
    profile_change.status = 'approved'
    profile_change.save()
    
    return redirect('profile_change_requests')



def deny_profile_change(request, change_id):
    profile_change = get_object_or_404(ProfileChange, pk=change_id)
    # Assuming you have a logic to handle denying changes here
    profile_change.status = 'denied'
    profile_change.save()
    return redirect('profile_change_requests') 
 




def student_upload_files(request, student_prn):
    student = get_object_or_404(Student, PRN=student_prn)
    
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_profile', student_prn=student_prn)
    else:
        form = UploadFilesForm(instance=student)
    
    return render(request, 'student_file_uploads.html', {'form': form, 'student': student})


@login_required
def profile(request):
    user_type = request.user.user_type

    if user_type == 'Coordinator':
        coordinator = Coordinator.objects.get(user=request.user)
        return render(request, 'profile.html', {'coordinator': coordinator})
        
    elif user_type == 'TNP-Office':
        tnpoffice = TNPOffice.objects.get(user=request.user)
        return render(request, 'profile.html', {'tnpoffice': tnpoffice})
    
        
    else:
        # Redirect to appropriate view if user is neither a coordinator nor TNP office member
        return redirect('login')  # Adjust this to your login URL
    



def register_student(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST,view_name='register_student')
        student_form = StudentForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()

            user.set_password(user_form.cleaned_data["password1"])
            user.save()
            Student.objects.create(user=user, **student_form.cleaned_data)
            print("DATA:",student_form.cleaned_data )
            user.backend = 'users.authentication.EmailBackend'             
            # login(request, user)
            return redirect('login')
                
        else:
            # Print form errors for debugging
            print("User Form Data:", user_form.cleaned_data)  # Print user form data
    else:
        user_form = CustomUserForm(view_name='register_student')
        student_form = StudentForm()

    return render(request, 'student_registration.html', {'user_form': user_form, 'student_form': student_form, })



@tnpoffice_required
def register_coordinator(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        coordinator_form = CoordinatorForm(request.POST, request.FILES)
        print("DATA:",coordinator_form)

        if user_form.is_valid() and coordinator_form.is_valid():

            user = user_form.save()
            user.set_password(user_form.cleaned_data["password1"])
            user.save()
            Coordinator.objects.create(user=user, **coordinator_form.cleaned_data)
            print("DATA:",coordinator_form.cleaned_data )
            user.backend = 'users.authentication.EmailBackend'             
            # login(request, user)
            return redirect('login')  # Redirect to the dashboard after successful registration
    else:
        user_form = CustomUserForm()
        coordinator_form = CoordinatorForm()
        
    return render(request, 'coordinator_registration.html', {'user_form': user_form, 'coordinator_form': coordinator_form, })

@login_required
@coordinator_required
def edit_coordinator_profile(request):
    # Get the coordinator object associated with the current user
    coordinator = get_object_or_404(Coordinator, user=request.user)

    if request.method == 'POST':
        form = CoordinatorForm(request.POST,request.FILES, instance=coordinator)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful edit
    else:
        form = CoordinatorForm(instance=coordinator)

    return render(request, 'edit_coordinator_profile.html', {'form': form})




def register_tnpoffice(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        tnpoffice_form = TNPOfficeForm(request.POST, request.FILES)
        if user_form.is_valid() and tnpoffice_form.is_valid():
            user = user_form.save()

            user.set_password(user_form.cleaned_data["password1"])
            user.save()
            TNPOffice.objects.create(user=user, **tnpoffice_form.cleaned_data)
            # print("DATA:",student_form.cleaned_data )
            user.backend = 'users.authentication.EmailBackend'             
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful registration
    else:
        user_form = CustomUserForm()
        tnpoffice_form = TNPOfficeForm()
        
    return render(request, 'tnpoffice_registration.html', {'user_form': user_form, 'tnpoffice_form': tnpoffice_form, })


@login_required
@tnpoffice_required
def edit_tnpoffice_profile(request):

    # Get the coordinator object associated with the current user
    tnpoffice = get_object_or_404(TNPOffice, user=request.user)

    if request.method == 'POST':
        form = TNPOfficeForm(request.POST,request.FILES, instance=tnpoffice)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful edit
    else:
        form = TNPOfficeForm(instance=tnpoffice)

    return render(request, 'edit_tnpoffice_profile.html', {'form': form})

from django.contrib.auth import authenticate
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():  # Check if form data is valid
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:  # Authentication successful
                login(request, user)
                return redirect('all-drives')  # Redirect to 'all-drives' upon successful login
            else:
                # Authentication failed (wrong credentials)
                messages.error(request, 'Wrong username or password')
                # No need to return here if authentication fails,
                # the form will still display the error message.
        else:
            # Form validation failed (invalid form data)
            messages.error(request, 'Wrong username or password')
            # Returning the form with errors to display them to the user

    else:
        # GET request or initial render of the login page
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        # If the request method is POST, it means the user has confirmed logout
        logout(request)
        # Redirect the user to the login page or any other page you prefer
        return redirect('login')
    else:
        # If the request method is not POST, render the logout confirmation page
        return render(request, 'logout.html')


@login_required
@student_not_required
def all_students(request):
    # Get the logged-in user
    user = request.user

    if user.user_type == 'TNP-Office':
        # tnpOffice user can see all students
        students = Student.objects.all()
    elif user.user_type == 'Coordinator':
        # Coordinator user can see students from their department
        if user.coordinator.department:
            students = Student.objects.filter(department=user.coordinator.department)
        else:
            # Handle case where coordinator has no department assigned
            students = Student.objects.none()
    else:
        # Handle other user types or unauthorized access
        students = Student.objects.none()  # Return empty queryset

    return render(request, 'all_students.html', {'students': students})
@login_required
@tnpoffice_required
def all_coordinators(request):
    coordinators = Coordinator.objects.all()
    return render(request, 'all_coordinators.html',{'coordinators': coordinators})


@login_required
@student_required
def apply_drive(request, drive_id):
    drive = get_object_or_404(Drive, drive_id=drive_id)
    student = request.user.student

    # Check if the student has already applied to this drive
    application = DriveApplication.objects.filter(student=student, drive=drive).first()
    if not application:
        # If the application doesn't exist, create a new DriveApplication object
        application = DriveApplication.objects.create(student=student, drive=drive)
        return redirect('application_success')
    else:
        # If the application exists, redirect to 'application_exists'
        return redirect('drive_application_exists')
    
@login_required
@student_required
def application_success(request):
    return render(request, 'application_success.html')

@login_required
@student_required
def drive_application_exists(request):
    return render(request, 'drive_application_exists.html')




@login_required
@coordinator_required

def applied_students_for_drive(request, drive_id):
    drive = get_object_or_404(Drive, pk=drive_id)
    coordinator = Coordinator.objects.get(user=request.user)  # Assuming each user has a corresponding coordinator entry
    drive_applications = DriveApplication.objects.filter(drive=drive, student__department=coordinator.department)
    
    # drive_applications = DriveApplication.objects.filter(drive=drive)
    round_names = [getattr(drive, f'round{i}') for i in range(1, 6)]
    if request.method == 'POST':
        for application in drive_applications:
            # Update round status and selection status based on form data
            application.round1 = bool(request.POST.get(f'round1_{application.id}', False))
            application.round2 = bool(request.POST.get(f'round2_{application.id}', False))
            application.round3 = bool(request.POST.get(f'round3_{application.id}', False))
            application.round4 = bool(request.POST.get(f'round4_{application.id}', False))
            application.round5 = bool(request.POST.get(f'round5_{application.id}', False))
            application.selected = bool(request.POST.get(f'selected_{application.id}', False))
            application.save()

        return redirect('drive_applied_students', drive_id=drive_id)

    applied_students = [application.student for application in drive_applications]

    return render(request, 'applied_students_for_drive.html', {'drive': drive,'drive_id': drive_id, 'applied_students': applied_students, 'drive_applications': drive_applications,'round_names': round_names,})

@login_required
def my_applications(request, student_prn):
    # Get the current logged-in student
    student = get_object_or_404(Student, PRN=student_prn)
    
    # Filter DriveApplication objects for the current student
    applied_drives = DriveApplication.objects.filter(student=student)
    
    # Prepare round information for each drive application
    drive_applications = []
    for application in applied_drives:
        round_info = {
            'drive': application.drive,
            'applied_date': application.applied_date,  # Include applied_date in context
            'round1': application.round1,
            'round2': application.round2,
            'round3': application.round3,
            'round4': application.round4,
            'round5': application.round5,
            'selected': application.selected,
        }
        drive_applications.append(round_info)
    
    # Filter ActivityApplication objects for the current student
    applied_activities = ActivityApplication.objects.filter(student=student)
    
    context = {
        'drive_applications': drive_applications,
        'applied_activities': applied_activities,
        'student': student
    }
    
    # Check user permissions and render the appropriate template
    if (request.user.user_type == 'Coordinator' or request.user.user_type == 'TNP-Office') \
        or (request.user.student.PRN == student_prn):
        return render(request, 'my_applications.html', context)
    else:
        return render(request, 'dashboard.html')  # Render appropriate dashboard template

@login_required
@student_required
def apply_activity(request, activity_id):
    activity = get_object_or_404(Activity, activity_id=activity_id)
    student = request.user.student

    # Check if the student has already applied to this drive
    application = ActivityApplication.objects.filter(student=student, activity=activity).first()
    if not application:
        # If the application doesn't exist, create a new DriveApplication object
        application = ActivityApplication.objects.create(student=student, activity=activity)
        return redirect('application_success')
    else:
        # If the application exists, redirect to 'application_exists'
        return redirect('activity_application_exists')

@login_required
@student_required
def activity_application_exists(request):
    
    return render(request, 'activity_application_exists.html')    

@login_required
@coordinator_required

def applied_students_for_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity_applications = ActivityApplication.objects.filter(activity=activity)
    applied_students = [application.student for application in activity_applications]
    return render(request, 'applied_students_for_activity.html', {'activity': activity, 'applied_students': applied_students,'activity_applications':activity_applications})


