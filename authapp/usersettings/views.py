from django.shortcuts import render, redirect
from authapp.forms import ProfileForm
from django.urls import reverse
from authapp.models import User, user_directory_path

def ProfileSettings(request):
    user = request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':

        form = ProfileForm(request.POST,request.FILES,instance=user)

        if form.is_valid():

            if request.POST.get("firstname"):
                try:
                    firstname = request.POST.get("firstname")
                    user.first_name = firstname
                except Exception as e:
                    print(e)

            if request.POST.get("lastname"):
                try:
                    lastname = request.POST.get("lastname")
                    user.last_name = lastname
                except Exception as e:
                    print(e)

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