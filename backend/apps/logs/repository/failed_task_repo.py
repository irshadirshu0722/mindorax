from apps.logs.models import FailedTaskAlert
from apps.utils import BaseRepository


class FailedTaskRepo(BaseRepository):
    def __init__(self):
        super().__init__(FailedTaskAlert)
