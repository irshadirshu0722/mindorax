import traceback

from apps.logs.repository import FailedTaskRepo


class FailedTaskService:
    def create_failed_task_alert(
        self,
        task_name,
        payload,
        error,
        traceback_text=None,
    ):
        if traceback_text is None:
            traceback_text = traceback.format_exc()
            if traceback_text == "NoneType: None\n":
                traceback_text = ""

        return FailedTaskRepo().create(
            task_name=task_name,
            payload=payload,
            error_message=str(error),
            traceback=traceback_text,
        )
