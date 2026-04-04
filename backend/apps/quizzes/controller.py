from ninja import Router,Query
from apps.permissions import IsAuthenticated
from .schemas import QuizCreate,QuizResponse,QuizAttemptCreate,ShortQuizResponse,QuizAttemptResponse
from .services import QuizService
from apps.utils import PaginationResponse
router = Router(auth=IsAuthenticated())

"""
Plan
-------
1 - User want to request to create quizzes by choosing topics as list
2 - User able to submit the quiz answer and response the result + Ai suggestion
3 - List all quizzes + Result + answer
4 - Full Review to get in which area he making mistakes
"""


@router.post("/{subject_id}")
def create_quizzes(request,subject_id:int,data:QuizCreate):
  QuizService().create_quiz_for_subject(request.user,subject_id,data.dict())

  return {
    "message": "Creating Quiz. It may take time"
  }

@router.get("/attempt/{quiz_id}",response=QuizResponse)
def get_quiz_details(request,quiz_id):
  print(QuizService().get_quiz_by_is_author(request.user,quiz_id))
  return QuizService().get_quiz_by_is_author(request.user,quiz_id)

@router.post("/report/{quiz_id}")
def request_ai_report(request,quiz_id):
  QuizService().create_ai_report(request.user,quiz_id)

  return {
    "message": "Creating Quiz AI Report. It may take time"
  }

@router.post("/submit/{quiz_id}",response=QuizAttemptResponse)
def create_quiz_attempt(request,quiz_id:int,data:QuizAttemptCreate):
  return QuizService().create_quiz_attempt(request.user,quiz_id,data.dict())

@router.get("/all/{subject_id}",response=PaginationResponse[ShortQuizResponse])
def get_all_quiz(request,subject_id,page:int=Query(1),page_size:int=Query(20)):
  return QuizService().get_all_quiz_by_pagination(request.user,subject_id,page,page_size)