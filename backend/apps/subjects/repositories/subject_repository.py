from apps.utils import BaseRepository
from apps.subjects.models import SubjectAnalyze,Subject
class SubjectRepository(BaseRepository):
  def __init__(self):
    super().__init__(Subject)


class SubjectAnalyzeRepository(BaseRepository):
  def __init__(self):
    super().__init__(SubjectAnalyze)
  def get_by_subject(self,subject):
    return self.model.objects.get(subject=subject)
