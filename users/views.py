from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserCustomForm, ProfileForm, SkillsForm
from .models import Profile
from django.contrib import messages
from .models import User
from django.http import HttpResponse

def registerUser(request):
    form = UserCustomForm()
    page = 'register'
    if request.method == 'POST':
        form = UserCustomForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = user.username.lower()
            user.save()
            messages.success(request, "Your account have created successfully!")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error occurred during registration!")
    context ={'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)

def loginUser(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect('profiles')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username or password is incorrect")
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')



def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    try:
        profile = Profile.objects.get(id=pk)
        topskills = profile.skills_set.exclude(description__exact="")
        otherskills = profile.skills_set.filter(description="")
    except Profile.DoesNotExist:
        # Handle the case when the profile does not exist
        return HttpResponse("Profile does not exist.")

    context = {
        'profile': profile,
        'topskills': topskills,
        'otherskills': otherskills,
    }
    return render(request, 'users/user-profile.html', context)

login_required(login_url='login')

login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skills_set.all()
    projects = profile.projects_set.all()
    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSKill(request):
    profile = request.user.profile    
    form = SkillsForm()

    if request.method == 'POST':        
        form = SkillsForm(request.POST)
        if form.is_valid():
            skills = form.save(commit=False)
            skills.owner = profile
            skills.save()
            messages.success(request, "Skill added successfuly")
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skills_form.html', context)


@login_required(login_url='login')
def updateSKill(request, pk):
    profile = request.user.profile  
    skill = profile.skills_set.get(id=pk)  
    form = SkillsForm(instance=skill)

    if request.method == 'POST':        
        form = SkillsForm(request.POST, instance=skill)
        if form.is_valid():
          
            form.save()
            messages.success(request, "Skill updated successfuly")
            return redirect('account')

    context = {'form':form,}
    return render(request, 'users/skills_form.html', context)


def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skills_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully")
        return redirect('account')
    context = {'object' : skill}
    return render(request, 'delete_template.html')