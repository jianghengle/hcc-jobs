from django.urls import path

from .views import job_view
from .views import account_view

urlpatterns = [
    path('login_user', account_view.login_user, name='login_user'),
    path('get_user', account_view.get_user, name='get_user'),

    path('get_squeue', job_view.get_squeue, name='get_squeue'),
    path('get_job_detail/<str:job_id>/', job_view.get_job_detail, name='get_job_detail'),
]
