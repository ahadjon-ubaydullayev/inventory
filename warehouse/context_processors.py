# myapp/context_processors.py
def profile_picture(request):
    if request.user.is_authenticated:
        return {
            'profile_pic': request.user.photo.url if request.user.photo else 'default-profile-pic-url'
        }
    return {}
