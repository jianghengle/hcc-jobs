from django.urls import path

from .views import question_view
from .views import csv_file_view
from .views import squeue_view
from .views import account_view

urlpatterns = [
    path('get_questions', question_view.get_questions, name='get_questions'),
    path('get_question/<int:question_id>', question_view.get_question, name='get_question'),
    path('create_question', question_view.create_question, name='create_question'),
    path('update_question/<int:question_id>', question_view.update_question, name='update_question'),
    path('delete_question', question_view.delete_question, name='delete_question'),

    path('get_csv/<filename>', csv_file_view.get_csv, name='get_csv'),
    path('request_squeue', squeue_view.request_squeue, name='request_squeue'),
    path('login_user', account_view.login_user, name='login_user')
]
