from apps.utils import BaseRepository
from subjects.models import SubjectExtract,Subject
class SubjectRepository(BaseRepository):
  def __init__(self):
    super().__init__(Subject)


class SubjectExtractRepository(BaseRepository):
  def __init__(self):
    super().__init__(SubjectExtract)

