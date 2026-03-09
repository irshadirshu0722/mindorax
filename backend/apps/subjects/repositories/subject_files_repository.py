from apps.utils import BaseRepository
from subjects.models import SubjectFile

class SubjectFileRepository(BaseRepository):
  def __init__(self):
    super().__init__(SubjectFile)

