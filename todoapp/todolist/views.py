from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import TaskForm
from . models import Task, User, SavedJob
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomRegistrationForm
from django.forms.utils import ErrorDict
from django.http import JsonResponse
import requests
from datetime import datetime, timedelta

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
# from jobspy import Site
# @login_required
# def job_post(request):
#     jobs = []
    
#     if request.method == "POST":
#         search_term = request.POST.get("search_term")
#         location = request.POST.get("location")
#         results_wanted = int(request.POST.get("results_wanted", 25))
#         hours_old = int(request.POST.get("hours_old", 72))
#         job_results = scrape_jobs(
#             site_name=[site.name for site in Site],
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



@login_required
def job_post(request):
    jobs = []

    if request.method == "POST":
        search_term = request.POST.get("search_term")
        location = request.POST.get("location")
        results_wanted = int(request.POST.get("results_wanted", 25))
        hours_old = int(request.POST.get("hours_old", 72))
        url = "https://jsearch.p.rapidapi.com/search"
        params = {
            "query": f"{search_term} in {location}",
            "country":"IN",
            "num_pages": (results_wanted // 10) + 1  # JSearch returns 10 results per page
        }

        headers = {
            "X-RapidAPI-Key": "1be6a49f5amsh74e11843fcdd1abp199396jsn1e7e53319589",
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            job_results = response.json().get("data", [])

            jobs = [
                {
                    "job_url": job.get("job_apply_link", "#"),
                    "title": job.get("job_title", "No Title"),
                    "company": job.get("employer_name", "No Company"),
                    "location":  f"{job.get('job_city', '')}, {job.get('job_state', '')}, {job.get('job_country', '')}".strip(", "),
                    "date_posted": job.get("job_posted_at", "No Date"),
                }
                for job in job_results[:results_wanted]  # Limit results
            ]

    return render(request, "job_post.html", {"jobs": jobs})

@login_required
def save_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("company")
        location = request.POST.get("location")
        date_posted = request.POST.get("date_posted")
        job_url = request.POST.get("job_url")

        # Check if the job is already saved
        job, created = SavedJob.objects.get_or_create(
            title=title,
            company=company,
            location=location,
            date_posted=date_posted,
            job_url=job_url,
            user=request.user,
        )

        return JsonResponse({"saved": created})  # Send response if job is saved

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def saved_jobs(request):
    jobs = SavedJob.objects.filter(user=request.user).order_by("-created")
    return render(request, "saved_jobs.html", {"jobs": jobs})

@login_required
def remove_job(request, job_id):
    if request.method == "POST":
        job = SavedJob.objects.filter(id=job_id, user=request.user).first()
        if job:
            job.delete()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)