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
    
            if request.FILES.get(user.profile_picture) == False:
                print("Modifying...")
                return user.profile_picture == "media/profile_picturedefault.png"
            else:
                print("profile_picture IS NOT NONE")

            form.save()
            return redirect(reverse('profile', kwargs={'username':user.username}))

    context = {"user":user,"form":form}

    return render(request,'useredit.html',context)