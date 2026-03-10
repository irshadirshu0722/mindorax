from apps.utils import BaseRepository
from apps.subjects.models import SubjectFile

class SubjectFileRepository(BaseRepository):
  def __init__(self):
    super().__init__(SubjectFile)

