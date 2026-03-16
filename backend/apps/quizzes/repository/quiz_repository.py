
from apps.utils import BaseRepository
from apps.quizzes.models import Quiz,QuizAttempts,QuizQuestionOption,QuizQuestion,QuizAttemptAnswer
class QuizRepo(BaseRepository):
  def __init__(self):
    super().__init__(Quiz)

class QuizQuestionRepo(BaseRepository):
  def __init__(self):
    super().__init__(QuizQuestion)

class QuizOptionRepo(BaseRepository):
  def __init__(self):
    super().__init__(QuizQuestionOption)

class QuizAttemptRepo(BaseRepository):
  def __init__(self):
    super().__init__(QuizAttempts)
class QuizAttemptAnswerRepo(BaseRepository):
  def __init__(self):
    super().__init__(QuizAttemptAnswer)