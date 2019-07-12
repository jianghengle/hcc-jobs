from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def json(self):
        return {
            "id": self.id,
            "questionText": self.question_text,
            "pubDate": str(self.pub_date)
        }

    @staticmethod
    def json_arr(questions):
        return [ q.json() for q in questions ]

    @staticmethod
    def get_by_id(question_id):
        return Question.objects.get(pk=question_id)

    @staticmethod
    def create(question):
        question.save()

    @staticmethod
    def update(question):
        question.save()

    @staticmethod
    def delete_by_id(question_id):
        question = Question.objects.get(pk=question_id)
        question.delete()
