from django.shortcuts import render, redirect
from authapp.forms import ProfileForm
from django.urls import reverse
from authapp.models import User, user_directory_path

def ProfileSettings(request):
    user = request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        print("Working on profile settings now...")
        form = ProfileForm(request.POST,request.FILES,instance=user)
        print(form.data)
        if form.is_valid():
            form.save(commit=False)

            # if request.FILES.get('avatar'):  # Check for uploaded avatar
            #     profile_form.avatar = request.FILES['avatar']

            # try:
            #     user.avatar.save(user_directory_path(user))
            # except Exception as e:
            #     print(e)
    
            if request.FILES.get(user.avatar) == False:
                print("Modifying...")
                return user.avatar == "media/avatardefault.png"
            else:
                print("AVATAR IS NOT NONE")

            form.save()
            return redirect(reverse('profile', kwargs={'username':user.username}))
    

    context = {"user":user,"form":form}

    return render(request,'useredit.html',context)

from image_cropping.utils import get_backend
# thumbnail_url = get_backend().get_thumbnail_url(
#     User.avatar,
#     {
#         'size': (430, 360),
#         'box': User.cropping,
#         'crop': True,
#         'detail': True,
#     }
# )