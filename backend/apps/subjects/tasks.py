from celery import shared_task
from celery.utils.log import get_task_logger
from apps.gemini import GeminiAPIService
from apps.logs.services import FailedTaskService
logger = get_task_logger(__name__)

MAX_RETRIES = 5
RETRY_BACKOFF_BASE = 2


@shared_task(
    bind=True,
    max_retries=MAX_RETRIES,
    default_retry_delay=RETRY_BACKOFF_BASE,
    acks_late=True,
    reject_on_worker_lost=True,
)
def analyze_subject_in_background(self, subject_id):
    from .services import SubjectService
    from .repositories import SubjectRepository

    subject = SubjectRepository().get(id=subject_id)
    subject_files = subject.files.all()
    SubjectService().update_subject_analyzing_status(subject, True, False)

    try:
        response = GeminiAPIService().run_analyze_subject(subject, subject_files)
        SubjectService().create_or_update_service_analyze(subject, response)
        SubjectService().update_subject_analyzing_status(subject, False, False)
        logger.info("Subject analyzed successfully | subject_id=%s", subject_id)

    except Exception as err:
        current_attempt = self.request.retries + 1
        logger.warning(
            "Subject analysis failed | subject_id=%s | attempt=%s/%s | error=%s",
            subject_id, current_attempt, MAX_RETRIES, str(err)
        )

        if self.request.retries < MAX_RETRIES:
            countdown = RETRY_BACKOFF_BASE ** current_attempt
            logger.info("Retrying in %ss | subject_id=%s", countdown, subject_id)
            raise self.retry(exc=err, countdown=countdown)

  
        logger.error(
            "DEAD LETTER | subject_id=%s exhausted all %s retries | error=%s",
            subject_id, MAX_RETRIES, str(err)
        )
        SubjectService().update_subject_analyzing_status(subject, False, True)
        FailedTaskService.create_failed_task_alert(
            task_name="analyze_subject_in_background",
            payload={"subject_id": subject_id},
            error=err,
        )


