from celery import shared_task
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
def create_subject_planning_in_background(self, subject_id,data):
    from apps.subjects.repositories import SubjectRepository
    from apps.planning.services  import StudyPlanService
    from apps.planning.repository import StudyPlanRepo
    subject = SubjectRepository().get(id=subject_id)
    data['subject'] = subject
    planning = StudyPlanRepo().create(**data)
    plan_id = planning.id
    try:
        response = GeminiAPIService().run_study_plan_create(subject, planning)
        StudyPlanService().update_creating_planning_status(planning, is_creating=False, is_failed=False)
        StudyPlanService().create_plan_items(planning,response)
        logger.info("Plan created successfully | plan_id=%s",plan_id )

    except Exception as err:
        current_attempt = self.request.retries + 1  # 1-indexed for readability
        logger.warning(
            "Study plan creation failed | plan_id=%s | attempt=%s/%s | error=%s",
            plan_id, current_attempt, MAX_RETRIES, str(err)
        )

        if self.request.retries < MAX_RETRIES:
            countdown = RETRY_BACKOFF_BASE ** current_attempt
            logger.info("Retrying in %ss | plan_id=%s", countdown, plan_id)
            raise self.retry(exc=err, countdown=countdown)

        logger.error(
            "DEAD LETTER | plan_id=%s exhausted all %s retries | error=%s",
            plan_id, MAX_RETRIES, str(err)
        )
        StudyPlanService().update_creating_planning_status(planning, is_creating=False, is_failed=True)
        # StudyPlanRepo().delete(planning)
        FailedTaskService().create_failed_task_alert(
            task_name="create_subject_planning_in_background",
            payload={"subject_id": subject_id, "plan_id": plan_id},
            error=err,
        )