from celery import shared_task
from kombu.exceptions import OperationalError
from apps.gemini import GeminiAPIService
from apps.logs.services import FailedTaskService
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

MAX_RETRIES = 5
RETRY_BACKOFF_BASE = 2  # seconds — exponential: 2, 4, 8, 16, 32


@shared_task(
    bind=True,
    max_retries=MAX_RETRIES,
    default_retry_delay=RETRY_BACKOFF_BASE,
    acks_late=True,           # task ack'd only after completion (safe retry on worker crash)
    reject_on_worker_lost=True,
)
def create_quiz_in_background(self, subject_id, quiz_id):
    from apps.subjects.repositories import SubjectRepository
    from .repository import QuizRepo
    from .services import QuizService

    subject = SubjectRepository().get(id=subject_id)
    quiz = QuizRepo().get(id=quiz_id)
    QuizService().update_creating_quiz_status(subject, is_creating=True, is_failed=False)

    try:
        response = GeminiAPIService().run_quiz_creation(subject, quiz)
        questions = response.get('questions')
        QuizService().create_quiz_question_from_response(quiz, questions)
        QuizService().update_creating_quiz_status(subject, is_creating=False, is_failed=False)
        logger.info("Quiz created successfully | quiz_id=%s", quiz_id)

    except Exception as err:
        current_attempt = self.request.retries + 1  # 1-indexed for readability
        logger.warning(
            "Quiz creation failed | quiz_id=%s | attempt=%s/%s | error=%s",
            quiz_id, current_attempt, MAX_RETRIES, str(err)
        )

        if self.request.retries < MAX_RETRIES:
            countdown = RETRY_BACKOFF_BASE ** current_attempt
            logger.info("Retrying in %ss | quiz_id=%s", countdown, quiz_id)
            raise self.retry(exc=err, countdown=countdown)

        logger.error(
            "DEAD LETTER | quiz_id=%s exhausted all %s retries | error=%s",
            quiz_id, MAX_RETRIES, str(err)
        )
        QuizService().update_creating_quiz_status(subject, is_creating=False, is_failed=True)
        QuizRepo().delete(quiz)
        FailedTaskService().create_failed_task_alert(
            task_name="create_quiz_in_background",
            payload={"subject_id": subject_id, "quiz_id": quiz_id},
            error=err,
        )


@shared_task(
    bind=True,
    max_retries=MAX_RETRIES,
    default_retry_delay=RETRY_BACKOFF_BASE,
    acks_late=True,
    reject_on_worker_lost=True,
)
def create_ai_report_in_background(self, quiz_id):
    from .repository import QuizRepo

    quiz = QuizRepo().get(id=quiz_id)
    QuizRepo().update(quiz, ai_report_creating=True)

    try:
        response = GeminiAPIService().run_ai_quiz_report()
        QuizRepo().update(quiz, ai_report=response)
        logger.info("Quiz AI Report created successfully | quiz_id=%s", quiz_id)

    except Exception as err:
        current_attempt = self.request.retries + 1
        logger.warning(
            "AI Report creation failed | quiz_id=%s | attempt=%s/%s | error=%s",
            quiz_id, current_attempt, MAX_RETRIES, str(err)
        )

        if self.request.retries < MAX_RETRIES:
            countdown = RETRY_BACKOFF_BASE ** current_attempt
            raise self.retry(exc=err, countdown=countdown)

        logger.error(
            "DEAD LETTER | quiz_id=%s AI report exhausted all %s retries | error=%s",
            quiz_id, MAX_RETRIES, str(err)
        )
        QuizRepo().update(quiz, ai_report_creating=False)
        FailedTaskService().create_failed_task_alert(
            task_name="create_ai_report_in_background",
            payload={"quiz_id": quiz_id},
            error=err,
        )

    finally:
        # Only mark as done if we're NOT retrying
        if self.request.retries >= MAX_RETRIES:
            from .repository import QuizRepo
            quiz = QuizRepo().get(id=quiz_id)
            QuizRepo().update(quiz, ai_report_creating=False)

