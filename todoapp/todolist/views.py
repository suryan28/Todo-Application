from django.shortcuts import render, HttpResponse, redirect
from .forms import TaskForm
from . models import Task, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomRegistrationForm
from django.forms.utils import ErrorDict


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but don't save it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            login(request, new_user)
            return redirect('/')  
    else:
        form = CustomRegistrationForm()
    # Handle validation error raised in the form's clean method
    if isinstance(form.errors, ErrorDict) and 'username' in form.errors:
        user_exists_error = form.errors["username"]
    else:
        user_exists_error = None
    return render(request, 'register.html', {'form': form, 'user_exists_error': user_exists_error})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  

@login_required
def index(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Associate task with current user
            task.save()
            return redirect("index")
    else:
        form = TaskForm()
    tasks = Task.objects.filter(user=request.user)  # Fetch tasks associated with current user
    return render(request, "index.html", {"task_form": form, "tasks": tasks})

@login_required
def update_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = TaskForm(instance=task)

    return render(request, "update_task.html", {"task_edit_form": form})

@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.delete()
    return redirect("index")


# from jobspy import scrape_jobs

# @login_required
# def job_post(request):
#     jobs = []
    
#     if request.method == "POST":
#         search_term = request.POST.get("search_term")
#         location = request.POST.get("location")
#         results_wanted = int(request.POST.get("results_wanted", 25))
#         hours_old = int(request.POST.get("hours_old", 72))

#         job_results = scrape_jobs(
#             site_name=["linkedin"],
#             search_term=search_term,
#             location=location,
#             results_wanted=results_wanted,
#             hours_old=hours_old,
#             country_indeed="India"
#         )

#         # Filter only required columns
#         jobs = [
#             {
#                 "job_url": job["job_url"],
#                 "title": job["title"],
#                 "company": job["company"],
#                 "location": job["location"],
#                 "date_posted": job["date_posted"],
#             }
#             for job in job_results.to_dict(orient="records")
#         ]

#     return render(request, "job_post.html", {"jobs": jobs})