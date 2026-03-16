import traceback

from apps.quizzes.repository import QuizAttemptRepo,QuizRepo,QuizOptionRepo,QuizQuestionRepo,QuizAttemptAnswerRepo
from apps.subjects.services import SubjectService
from apps.subjects.repositories import SubjectRepository
from apps.quizzes.tasks import create_quiz_in_background,create_ai_report_in_background
from django.core.exceptions import ObjectDoesNotExist
from ninja.errors import HttpError
class QuizService:
  def __int__(self):
    self.quiz_repo = QuizRepo()
    self.quiz_attempt_repo = QuizAttemptRepo()
    self.quiz_question_option_repo = QuizOptionRepo()
    self.quiz_attempt_answer_repo = QuizAttemptAnswerRepo()
  
  def create_quiz_for_subject(self,user,subject_id,data):
    subject = SubjectRepository().get_with_is_author(user,id=subject_id)
    data['subject'] = subject
    quiz = QuizRepo().create(**data)

    create_quiz_in_background.delay(subject_id=subject_id,quiz_id=quiz.id)
  
  def create_quiz_question_from_response(self,quiz,questions):
    for question in questions:
      question['quiz'] = quiz
      options = question.pop('options')
      question_instance = QuizQuestionRepo().create(**question)
      for option in options:
        option['question'] = question_instance
        QuizOptionRepo().create(**option)
  
  def update_creating_quiz_status(self,subject,**data):
    SubjectRepository().update(subject,**data)

  def get_quiz_by_is_author(self,user,quiz_id):
    try:
      quiz = QuizRepo().get(id=quiz_id)
      subject = quiz.subject
      
    except ObjectDoesNotExist:
      raise HttpError(status_code=404,message="Quiz is not found")
    if subject.user_id != user.id:
      raise HttpError(status_code=403,message="You are not allowed to attempt this quiz")
    return quiz
  
  def create_quiz_attempt(self,user, quiz_id, data):
    try:
      quiz = self.get_quiz_by_is_author(user,quiz_id)
      quiz_attempt = QuizAttemptRepo().create(quiz = quiz)

      attempts = data.get('answers')
      time_taken = data.get('time_taken')
      score = self._create_attempts_and_score(quiz,quiz_attempt,attempts)

      QuizAttemptRepo().update(quiz_attempt,score=score,total_score=len(attempts),time_taken=time_taken)
    except:
      quiz_attempt.delete()
      raise HttpError(status_code=500,message="Failed to submit quiz, Please try again later")
    return quiz_attempt
    

  def create_ai_report(self,user,quiz_id):
    quiz = self.get_quiz_by_is_author(user,quiz_id)
    create_ai_report_in_background.delay(quiz_id=quiz_id)

  def get_all_quiz(self,user,subject_id):
    subject = SubjectService().get_subject_with_is_author(user,subject_id)

    quizzes = QuizRepo().filter(subject=subject).all()
    return quizzes

  def _attempt_data_to_dict(self,attempts):
    return {item['question_id']:item['option_id'] for item in attempts}

  def _create_attempts_and_score(self,quiz,quiz_attempt,attempts):
    try:
      mapped_attempts  = self._attempt_data_to_dict(attempts)
      if quiz.questions.count() != len(attempts):
        raise ValueError("Number of given questions must be equal quiz questions")
      score = 0
      questions = quiz.questions.all()
      for q in questions:
        selected_option = mapped_attempts.get(q.id)
        option_instance = QuizOptionRepo().get(id=selected_option,question=q)
        is_correct = option_instance.is_correct
        score += is_correct
        QuizAttemptAnswerRepo().create(attempt=quiz_attempt, question = q,selected_option=option_instance,is_correct=is_correct)
    except Exception as e:
      traceback.print_exc()
      raise HttpError(status_code=400,message="Attempt failed because some question not found")
    return score