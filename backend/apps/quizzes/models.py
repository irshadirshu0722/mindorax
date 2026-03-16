from django.db import models
from apps.utils import CreateUpdateAt,DIFFICULTY_LEVEL_CHOICES
from apps.subjects.models import Subject
from apps.users.models import User

QUESTION_TYPE_CHOICES = (
    ("single", "Single Correct Answer"),
    ("multiple", "Multiple Correct Answers"),
)

class Quiz(CreateUpdateAt):
  DIFFICULTY_LEVEL_CHOICES = [*DIFFICULTY_LEVEL_CHOICES,('mixed','Mixed')]
  subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="quizzes")
  topics = models.JSONField()
  difficulty_level = models.CharField(choices=DIFFICULTY_LEVEL_CHOICES)
  total_questions = models.IntegerField()
  is_creating = models.BooleanField(default=False)
  is_failed = models.BooleanField(default=False)
  ai_report  = models.TextField()
  ai_report_creating = models.BooleanField(default=False)


class QuizQuestion(CreateUpdateAt):
  quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions")
  question_text = models.TextField()
  explanation = models.TextField()
  difficulty = models.CharField(max_length=20,choices=DIFFICULTY_LEVEL_CHOICES)
  topic = models.CharField(max_length=200)
  question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES,default='single')

  def is_correct_option(self, option_id):

    return self.options.filter(id=option_id, is_correct=True).exists()

class QuizQuestionOption(CreateUpdateAt):
  question = models.ForeignKey(QuizQuestion,on_delete=models.CASCADE,related_name="options")
  text = models.TextField()
  is_correct = models.BooleanField()

class QuizAttempts(CreateUpdateAt):
  quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="attempts")
  score = models.IntegerField(default=0,)
  total_score = models.IntegerField(default=0)
  time_taken = models.IntegerField(default=0)

class QuizAttemptAnswer(CreateUpdateAt):
    attempt = models.ForeignKey(
        QuizAttempts,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE
    )
    selected_option = models.ForeignKey(
        QuizQuestionOption,
        on_delete=models.CASCADE
    )
    is_correct = models.BooleanField()