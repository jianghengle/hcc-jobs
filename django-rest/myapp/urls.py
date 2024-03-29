from django.urls import path
from .views import account_view
from .views import job_view
from .views import file_view
from .views import jupyter_view

urlpatterns = [
    path('login_user', account_view.login_user, name='login_user'),
    path('get_user', account_view.get_user, name='get_user'),
    path('change_password', account_view.change_password, name='change_password'),

    path('get_jobs/<str:start_date>', job_view.get_jobs, name='get_jobs'),
    path('get_job_detail/<str:job_id>/', job_view.get_job_detail, name='get_job_detail'),
    path('submit_job', job_view.submit_job, name='submit_job'),
    path('cancel_job', job_view.cancel_job, name='cancel_job'),

    path('get_directory/<path:path>', file_view.get_directory, name='get_directory'),
    path('get_file/<path:path>', file_view.get_file, name='get_file'),
    path('create_file', file_view.create_file, name='create_file'),
    path('create_directory', file_view.create_directory, name='create_directory'),
    path('update_file_directory', file_view.update_file_directory, name='update_file_directory'),
    path('delete_file_directory', file_view.delete_file_directory, name='delete_file_directory'),
    path('upload_file/<path:path>', file_view.upload_file, name='upload_file'),
    path('update_text/<path:path>', file_view.update_text, name='update_text'),
    path('get_download_link/<path:path>', file_view.get_download_link, name='get_download_link'),
    path('paste_file_directory', file_view.paste_file_directory, name='paste_file_directory'),

    path('get_jupyters/<str:cluster>', jupyter_view.get_jupyters, name='get_jupyters'),
    path('start_jupyter', jupyter_view.start_jupyter, name='start_jupyter'),
    path('stop_jupyter', jupyter_view.stop_jupyter, name='stop_jupyter'),
]
