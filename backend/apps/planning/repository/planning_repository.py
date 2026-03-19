from apps.utils import BaseRepository
from apps.planning.models import PlanItems,StudyPlan,StudySession
class StudyPlanRepo(BaseRepository):
  def __init__(self, model=None):
    super().__init__(StudyPlan)
class PlanItemRepo(BaseRepository):
  def __init__(self, model=None):
    super().__init__(PlanItems)
class StudySessionRepo(BaseRepository):
  def __init__(self, model=None):
    super().__init__(StudySession)
    
