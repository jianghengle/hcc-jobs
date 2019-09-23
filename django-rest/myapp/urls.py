from django.urls import path
from .views import account_view
from .views import job_view
from .views import file_view

urlpatterns = [
    path('login_user', account_view.login_user, name='login_user'),
    path('get_user', account_view.get_user, name='get_user'),

    path('get_jobs/<str:start_date>', job_view.get_jobs, name='get_jobs'),
    path('get_job_detail/<str:job_id>/', job_view.get_job_detail, name='get_job_detail'),
    path('cancel_job', job_view.cancel_job, name='cancel_job'),

    path('get_file/<path:path>', file_view.get_file, name='get_file'),
    path('create_file', file_view.create_file, name='create_file'),
]
