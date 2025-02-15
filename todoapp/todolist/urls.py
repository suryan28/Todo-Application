from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path("update/<int:pk>/", views.update_task, name="update_task"),
    path("delete/<int:pk>/", views.delete_task, name="delete_task"),
    # path("job-post/", views.job_post, name="job_post")

]