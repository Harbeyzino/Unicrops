from .models import Profile

def user_profile(request):
    """Make user profile available in all templates"""
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'profile': profile}
    return {}
