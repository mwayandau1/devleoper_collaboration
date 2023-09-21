from django.shortcuts import render, redirect
from .models import Projects, Tag
from .forms import ProjectsForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import searchProject, paginateProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage




def projects(request):
    
    projects, search_query = searchProject(request) 
    results = 6
    projects, custom_pag = paginateProjects(request, projects, results)
    
    context = {
        'projects':projects,
        'search_query':search_query,
        'custom_pag':custom_pag,
    }
    return render(request, 'projects/projects.html',context)


def project(request, pk):
    project = Projects.objects.get(id=pk)
    
    context = {
        'project':project
    }
    return render(request, 'projects/single_project.html', context)

@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile

    form = ProjectsForm()
    if request.method == 'POST':
        form = ProjectsForm(request.POST, request.FILES)
        if form.is_valid():
            projects = form.save(commit=False)
            projects.owner = profile
            projects.save()
            form.save()
            messages.success(request,  "Project created successfuly!")
            return redirect('account')
    else:
       pass
    context = {
        'form': form,
        
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    form = ProjectsForm(instance=project)
    if request.method == 'POST':
        form = ProjectsForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfuly!")
            return redirect('account')
    context ={'form':form}
    return render(request, 'projects/project_form.html', context)





@login_required(login_url='login')
def deleteProject(request, id):
    profile = request.user.profile
    project = profile.projects_set.get(id=id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfuly!")
        return redirect('projects')
            
    context = { 'object': project}
    return render(request, 'delete_template.html', context)







