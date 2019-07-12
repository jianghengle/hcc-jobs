from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Question


@api_view(['Get'])
def get_questions(request):
    questions = Question.objects.all()
    return Response(Question.json_arr(questions))

@api_view(['Get'])
def get_question(request, question_id):
    question = Question.get_by_id(question_id)
    return Response(question.json())

@api_view(['Post'])
def create_question(request):
    question_text = request.data['questionText']
    question = Question(question_text=question_text, pub_date=timezone.now())
    Question.create(question)
    return Response(question.json())

@api_view(['Post'])
def update_question(request, question_id):
    question = Question.get_by_id(question_id)
    question.question_text = request.data['questionText']
    Question.update(question)
    return Response(question.json())

@api_view(['Post'])
def delete_question(request):
    question_id = request.data['questionId']
    Question.delete_by_id(question_id)
    return Response({'ok': True})