from django.shortcuts import render, redirect, get_object_or_404
from authapp.forms import ProfileForm
from django.urls import reverse
from authapp.models import User, user_directory_path

def ProfileSettings(request):
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':

        form = ProfileForm(request.POST,request.FILES,instance=user)

        if form.is_valid():
            if request.POST.get("lastname"):
                try:
                    lastname = request.POST.get("lastname")
                    user.last_name = lastname
                except Exception as e:
                    print(e)

            usersv = form.save(commit=False)

            if request.FILES.get("profile_picture"):
                print(request.FILES.get("profile_picture"))
                print(user.profile_picture)
                try:
                    profile_picture = request.FILES.get("profile_picture")
                    user.profile_picture == profile_picture
                    print(user.profile_picture)
                except Exception as e:
                    print(e)
            try:
                usersv.save()
                return redirect('home')
            except Exception as e:
                print(e)

            # if request.FILES.get(user.profile_picture) == None:
            #     print("Modifying...")
            #     return user.profile_picture == "media/profile_picturedefault.png"
            
            
            
            return redirect(reverse('profile', kwargs={'username':user.username}))

    context = {"user":user,"form":form}

    return render(request,'useredit.html',context)


def userNameInput(request):
    user = request.user
    form = ProfileForm(request.POST,request.FILES,instance=user)
    if user.name:
        return redirect(reverse('profile', kwargs={'username':user.username}))
    
    if user.name == None:
        if request.method == 'POST':
            action = request.POST.get("button-userinput")
            if action == 'refuse':
                redirect('userbioinputpage')

            if request.POST.get("name"):
                if form.is_valid():
                    try:
                        name = request.POST.get("name")
                        user.name = name
                        form.save()
                    except Exception as e:
                        print(e)
  
    return render(request,'editname.html',{'user':user,'form':form})
                
def userNameInput(request):
    user = request.user
    form = ProfileForm(request.POST,request.FILES,instance=user)
    if user.name:
        return redirect(reverse('profile', kwargs={'username':user.username}))
    
    if user.name == None:
        if request.method == 'POST':
            action = request.POST.get("button-userinput")
            if action == 'refuse':
                redirect('userbioinputpage')

            if request.POST.get("name"):
                if form.is_valid():
                    try:
                        name = request.POST.get("name")
                        user.name = name
                        form.save()
                    except Exception as e:
                        print(e)
  
    return render(request,'editname.html',{'user':user,'form':form})
                
'''Logout of your account'''