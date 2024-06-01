from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('all-students/', views.all_students, name='all_students'),
    path('all-coordinators/', views.all_coordinators, name='all_coordinators'),
    path('register-student/', views.register_student, name='register-student'),
    path('register-coordinator/', views.register_coordinator, name='register-coordinator'),
    path('register-tnpoffice/', views.register_tnpoffice, name='register-tnpoffice'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student-profile/<int:student_prn>/', views.student_profile, name='student_profile'),
    path('profile/edit_coordinator/', views.edit_coordinator_profile, name='coordinator_edit'),
    path('profile/edit_tnpoffice/', views.edit_tnpoffice_profile, name='tnpoffice_edit'),
  
    path('profile/', views.profile, name='profile'),
    path('upload-files/<str:student_prn>/', views.student_upload_files, name='upload_files'),
    path('edit_student_profile/<int:student_prn>/', views.edit_student_profile, name='edit_student_profile'),
    path('change_requests/', views.profile_changes_for_coordinator, name='profile_change_requests'),
    path('approve_profile_change/<int:change_id>/', views.approve_profile_change, name='approve_profile_change'),
    path('deny_profile_change/<int:change_id>/', views.deny_profile_change, name='deny_profile_change'),

    path('apply-drive/<int:drive_id>/', views.apply_drive, name='apply_drive'),
    path('application/success/', views.application_success, name='application_success'),
    path('drive/application/exists/', views.drive_application_exists, name='drive_application_exists'),
    path('drive/applied_students/<int:drive_id>/', views.applied_students_for_drive, name='drive_applied_students'),
    path('my_applications/<int:student_prn>/', views.my_applications, name='my_applications'),

    path('apply-activity/<int:activity_id>/', views.apply_activity, name='apply_activity'),
    path('activity/application/exists/', views.activity_application_exists, name='activity_application_exists'),
    path('activity/applied_students/<int:activity_id>/', views.applied_students_for_activity, name='activity_applied_students'),



    path('search/', views.search_students, name='search_students'),

  path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), 
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
]

