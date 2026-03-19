
from apps.planning.repository import StudySessionRepo,PlanItemRepo,StudyPlanRepo
from apps.subjects.services import SubjectService
from ninja.errors import HttpError
class StudyPlanService:

  def create_study_plan(self,user,subject_id,data):
    subject = SubjectService().get_subject_with_is_author(user,subject_id)
    
  def update_creating_planning_status(planning,**data):
    StudyPlanRepo().update(planning,**data)
  
  def create_plan_items(self,plan,data):
    plan_items = data.pop('plan_items')
    StudyPlanRepo().update(plan,**data)
    for item in plan_items:
      item['plan'] = plan
      PlanItemRepo().create(**item)
    return plan


  def get_all_plan_of_subject(self,user,subject_id):
    subject = SubjectService().get_subject_with_is_author(user,subject_id)

    return subject.study_plans.all()
  
  def get_plan_with_is_author(self,user,plan_id):
    try:
      plan = StudyPlanRepo().get(id=plan_id)
    except:
      raise HttpError(status_code=404,message="Plan not found")
    subject = plan.subject
    if subject.user != user:
      raise HttpError(status_code=503,message="You don't have access to this plan")
    return plan
  
  def get_plan_item_with_is_author(self,user,plan_item_id):
    try:
      plan_item = PlanItemRepo().get(id=plan_item_id)
    except:
      raise HttpError(status_code=404,message="Plan not found")
    subject = plan_item.plan.subject
    if subject.user != user:
      raise HttpError(status_code=503,message="You don't have access to this plan")
    return plan_item
  def create_study_plan_session(self,user,plan_item_id,data):
    plan_item = self.get_plan_item_with_is_author(user,plan_item_id)
    data['plan_item'] = plan_item
    return StudySessionRepo().create(**data)
    