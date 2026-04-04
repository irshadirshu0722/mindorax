from ninja import ModelSchema,Schema
from .models import Quiz,QuizAttempts,QuizQuestionOption,QuizQuestion
# from .models import 

class QuizCreate(ModelSchema):

  class Meta:
    model = Quiz
    fields = ['topics','difficulty_level','total_questions']

class QuizOptionsResponse(ModelSchema):
  class Meta:
    model = QuizQuestionOption
    fields = '__all__'

class QuestionQuestionResponse(ModelSchema):
  options : list[QuizOptionsResponse]=[]
  class Meta:
    model = QuizQuestion
    fields = '__all__'

class QuizResponse(ModelSchema):
  questions : list[QuestionQuestionResponse] = []
  class Meta:
    model = Quiz
    fields = '__all__'

class QuizAttemptCreateItem(Schema):
  question_id:int
  option_id:int

class QuizAttemptCreate(Schema):
  answers : list[QuizAttemptCreateItem]
  time_taken: int

class QuizAttemptResponse(ModelSchema):

  class Meta:
    model = QuizAttempts
    fields = "__all__"

class ShortQuizResponse(ModelSchema):
  attempted: bool = False
  class Meta:
    model = Quiz
    fields = '__all__'
  @staticmethod
  def resolve_attempted(obj, context):
      return obj.attempts.count() > 0