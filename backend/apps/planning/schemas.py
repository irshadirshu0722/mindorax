from ninja import ModelSchema,Schema
from datetime import datetime
from apps.planning.models import PlanItems,StudyPlan,StudySession

class StudyPlanCreate(Schema):
  topics: list[str]
  end_date: datetime
  starting_date: datetime
  description: str

class StudyPlanSessionResponse(ModelSchema):

  class Meta:
    model = StudySession
    fields = '__all__'


class StudyPlanItemsResponse(ModelSchema):
  plan_session:StudyPlanSessionResponse = None
  class Meta:
    model = PlanItems
    fields = '__all__'

class StudyPlanResponse(ModelSchema):
  plan_items:list[StudyPlanItemsResponse]=[]
  
  class Meta:
    model = StudyPlan
    fields = '__all__'
class StudyPlanListResponse(ModelSchema):
  class Meta:
    model = StudyPlan
    fields = '__all__'


class StudyPlanSessionCreate(ModelSchema):

  class Meta:
    model = StudySession
    fields = ['start_date_time','end_date_time']