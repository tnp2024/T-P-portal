from users.models import Coordinator, Student, TNPOffice

def sidebar_profile(request):
    user_profile = None
    if request.user.is_authenticated:
        if request.user.user_type == 'Coordinator':
            user_profile = Coordinator.objects.get(user=request.user)
        elif request.user.user_type == 'Student':
            user_profile = Student.objects.get(user=request.user)
        elif request.user.user_type == 'TNP-Office':
            user_profile = TNPOffice.objects.get(user=request.user)
    
    return {'user_profile': user_profile}
