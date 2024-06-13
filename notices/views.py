from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.staticfiles import finders  # Import finders to locate static files
from .models import Drive  # Import the Drive model
from reportlab.lib.enums import TA_CENTER,TA_RIGHT
from django.shortcuts import render,redirect,get_object_or_404
from .models import Drive,Activity,Department,Booklets
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import DriveForm,ActivityForm,BookletForm
# Create your views here.

from functools import wraps

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'Student':
            return HttpResponseForbidden("You don't have permission to access this view.")
        return view_func(request, *args, **kwargs)
    return wrapper

def student_not_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.user_type == 'Student':
            return HttpResponseForbidden("You don't have permission to access this view.")
        return view_func(request, *args, **kwargs)
    return wrapper

def coordinator_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'Coordinator':
            return HttpResponseForbidden("You don't have permission to access this view.")
        return view_func(request, *args, **kwargs)
    return wrapper
    

def tnpoffice_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'TNP-Office':
            return HttpResponseForbidden("You don't have permission to access this view.")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def dashboard(request):
    drive_count = Drive.objects.count()
    activity_count = Activity.objects.count()
    context = {'drve_count':drive_count,'activity_count':activity_count}
    return render(request,'dashboard.html',context)

def sidebar (request):
    context = {'user': request.user}
    return render(request,'sidebar.html',context)


@login_required
def drives(request):
    alldrives = Drive.objects.all()
    return render(request, 'all-drives.html', {'alldrives': alldrives})
    
@login_required
def drive(request, pk):
    drive = Drive.objects.get(drive_id=pk)
    return render(request, 'single-drive.html', {'drive': drive})  

@login_required
def download_drive_pdf(request, pk):
    # Retrieve the Drive object based on the drive ID
    drive = get_object_or_404(Drive, drive_id=pk)

    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{drive.title}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    style_bold = styles["Normal"]
    style_bold.fontName = 'sans-serif'  
    style_bold.fontSize = 14 

    # Prepare data for the PDF
    data = []
    # Add top margin from the logo
    header_image_path = finders.find('images/header.jpg')  # Assuming static folder
    if header_image_path:
        header_img = Image(header_image_path, width=100, height=50)
        data.append(header_img)
        data.append(Spacer(1, 20))  # Add space below header image

    centered_style = ParagraphStyle('centered_style', fontSize=12, alignment=TA_CENTER)
    Header_lines = (
        f'MGM University',
        f'Chhatrapati Sambhajinagar',
        f'Training and Placement Department',
        f'Jawaharlal Nehru Engineering College',
        f'___________________________________________________________________'
    )
    for line in Header_lines:
        data.append(Paragraph(line, centered_style))
        data.append(Spacer(1, 9))
    # Add header image from static directory
    # if drive.company_logo:
    #     company_logo_path = drive.company_logo.path
    #     company_logo_img = Image(company_logo_path, width=100, height=50)
    #     data.append(company_logo_img)

    date_style = ParagraphStyle('date_style', fontSize=10, bold=True,alignment=TA_RIGHT)        
    data.append(Paragraph(f"<strong>Shared On Date:</strong> {drive.creation_date.strftime('%d %B, %Y')}", date_style))  # Format date
    data.append(Spacer(1, 5))  # Add space between fields
    # Drive details

    detail_style = ParagraphStyle('detail_style', fontSize=10, bold=True) 

    data.append(Paragraph(f"<strong>Reference Number:</strong> {drive.Reference_no}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields  

    data.append(Paragraph(f"<strong>Campus Placement Drive by:</strong> {drive.company_name}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields




    data.append(Paragraph(f"<strong>Drive Date:</strong> {drive.date.strftime('%d %B, %Y')}", detail_style))  # Format date
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>About:</strong> {drive.content}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>Job CTC:</strong> {drive.job_CTC}", detail_style))
    data.append(Spacer(1, 5))

    data.append(Paragraph(f"<strong>Bond:</strong> {drive.Bond}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>Industry Type:</strong> {drive.industry_type}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields


    # Departments
    department_list = ", ".join([department.name for department in drive.department.all()])
    data.append(Paragraph(f"<strong>Departments:</strong> {department_list}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields


    data.append(Paragraph(f"<strong>Job Role:</strong> {drive.job_role}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>Job Location:</strong> {drive.job_location}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>Job Eligibility:</strong> {drive.job_eligibility}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>Selection Process:</strong> {drive.job_description}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>Number of Rounds:</strong> {drive.num_rounds}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>Round 1:</strong> {drive.round1}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields
    data.append(Paragraph(f"<strong>Round 2:</strong> {drive.round2}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields
    data.append(Paragraph(f"<strong>Round 3:</strong> {drive.round3}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields
    data.append(Paragraph(f"<strong>Round 4:</strong> {drive.round4}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields
    data.append(Paragraph(f"<strong>Round 5:</strong> {drive.round5}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields
  # Add space between fields


    # Application Link with hyperlink
    application_link_text = f"<strong>Application Link:</strong> <a href='{drive.application_link}' color='blue' >'{drive.application_link}'</a>"
    data.append(Paragraph(application_link_text, detail_style))
    data.append(Spacer(1, 40))  # Add space between fields

    # Add company logo image from media directory


    # Footer
    footer_style = ParagraphStyle('footer_style', fontSize=10, alignment=TA_RIGHT)
    footer_text = (
        f'_________________________________________________________________________________',
        f"Dr. Parminder Kaur",
        f"Head, Training and Placement",
        f"MGM University",
  
    )
    for line in footer_text:
        data.append(Paragraph(line, footer_style))
        data.append(Spacer(1, 8))
    
    # Build PDF document
    doc.build(data)
    
    return response
@login_required
@tnpoffice_required 

def createDrive(request):
    if request.method == 'POST':
        form = DriveForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-drives')  # Redirect to a success page or any other URL
    else:
        form = DriveForm()
    return render(request, 'create_drive.html', {'form': form})

# views.py


@login_required
@tnpoffice_required 

def updateDrive(request, pk):
    drive = get_object_or_404(Drive, drive_id=pk)
    form = DriveForm(instance=drive)
    if request.method == 'POST':
        form = DriveForm(request.POST, request.FILES, instance=drive)
        if form.is_valid():
            form.save()
            return redirect('all-drives')  # Redirect to any appropriate URL
    context = {'form': form}
    return render(request, 'create_drive.html', context)

@login_required
@tnpoffice_required 

def delete_Drive(request, pk):
    drive = get_object_or_404(Drive, drive_id=pk)
    if request.method == 'POST':
        drive.delete()
        return redirect('all-drives')
    context ={'drive': drive}
    return render(request, 'delete_drive.html', context)


#--------------------------------------- ACTIVITY VIEWS------------------------------------------
@login_required
def activities(request):
    activities = Activity.objects.all()
    context ={'activities':activities}
    return render(request, 'activities.html', context)
@login_required
def activity(request, pk):
    activity = Activity.objects.get(activity_id=pk)
    context={'activity':activity}
    return render(request, 'activity.html',context)  


@login_required
def download_activity_pdf(request, pk):
    # Retrieve the Drive object based on the drive ID
    activity = get_object_or_404(Activity, activity_id=pk)

    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{activity.title}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    style_bold = styles["Normal"]
    style_bold.fontName = 'sans-serif'  
    style_bold.fontSize = 14 

    # Prepare data for the PDF
    data = []
    # Add top margin from the logo
    header_image_path = finders.find('images/header.jpg')  # Assuming static folder
    if header_image_path:
        header_img = Image(header_image_path, width=100, height=50)
        data.append(header_img)
        data.append(Spacer(1, 20))  # Add space below header image

    centered_style = ParagraphStyle('centered_style', fontSize=12, alignment=TA_CENTER)
    Header_lines = (
        f'MGM University',
        f'Chhatrapati Sambhajinagar',
        f'Training and Placement Department',
        f'Jawaharlal Nehru Engineering College',
        f'___________________________________________________________________'
    )
    for line in Header_lines:
        data.append(Paragraph(line, centered_style))
        data.append(Spacer(1, 9))
    # Add header image from static directory
    # if drive.company_logo:
    #     company_logo_path = drive.company_logo.path
    #     company_logo_img = Image(company_logo_path, width=100, height=50)
    #     data.append(company_logo_img)

    date_style = ParagraphStyle('date_style', fontSize=10, bold=True,alignment=TA_RIGHT)        
    data.append(Paragraph(f"<strong>Shared On Date:</strong> {activity.creation_date.strftime('%d %B, %Y')}", date_style))  # Format date
    data.append(Spacer(1, 5))  # Add space between fields
    # Drive details

    detail_style = ParagraphStyle('detail_style', fontSize=10, bold=True) 

    data.append(Paragraph(f"<strong>Reference Number:</strong> {activity.Reference_no}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields  

    data.append(Paragraph(f"<strong>Campus Placement Preparation Activity by:</strong> {activity.company_name}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields




    data.append(Paragraph(f"<strong>Activity Date:</strong> {activity.activity_date.strftime('%d %B, %Y')}", detail_style))  # Format date
    data.append(Spacer(1, 5))  # Add space between fields

    data.append(Paragraph(f"<strong>About:</strong> {activity.content}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields


    data.append(Paragraph(f"<strong>Industry Type:</strong> {activity.industry_type}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields


    # Departments
    department_list = ", ".join([department.name for department in activity.department.all()])
    data.append(Paragraph(f"<strong>Departments:</strong> {department_list}", detail_style))
    data.append(Spacer(1, 5))  # Add space between fields





    # Footer
    footer_style = ParagraphStyle('footer_style', fontSize=10, alignment=TA_RIGHT)
    footer_text = (
        f'_________________________________________________________________________________',
        f"Dr. Parminder Kaur",
        f"Head, Training and Placement",
        f"MGM University",
  
    )
    for line in footer_text:
        data.append(Paragraph(line, footer_style))
        data.append(Spacer(1, 8))
    
    # Build PDF document
    doc.build(data)
    
    return response



@login_required
@tnpoffice_required 

def createActivity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('activities')  # Redirect to a success page or any other URL
    else:
        form = ActivityForm()
        context={'form':form}
    return render(request, 'create_activity.html', context)
@login_required
@tnpoffice_required 

def updateActivity(request, pk):
    activity = get_object_or_404(Activity, activity_id=pk)
    form = ActivityForm(instance=activity)
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activities')  # Redirect to any appropriate URL
    context = {'form': form}
    return render(request, 'create_activity.html', context)

@tnpoffice_required 
def delete_Activity(request, pk):
    activity = get_object_or_404(Activity, activity_id=pk)
    if request.method == 'POST':
        activity.delete()
        return redirect('activities')  # Redirect to any appropriate URL
    context={'activity':activity}
    return render(request, 'delete_activity.html', context)

@student_not_required
def upload_booklet(request):
    if request.method == 'POST':
        form = BookletForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all-booklets') 
    else:
        form = BookletForm()
    return render(request, 'upload_booklet.html', {'form': form})




def list_booklets(request):
    departments = Department.objects.prefetch_related('booklets_set').all()
    return render(request, 'list_booklets.html', {'departments': departments})