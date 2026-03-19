
from ninja import NinjaAPI
from .schemas import StudyPlanCreate,StudyPlanResponse,StudyPlanSessionCreate,StudyPlanSessionResponse
from .services import StudyPlanService
from apps.permissions import IsAuthenticated
"""
1 - Create Plan
2 - All Plan listing
3 - get a plan
4 - complete one task in a plan
"""

router = NinjaAPI(auth=IsAuthenticated())

@router("/create/{subject_id}")
def create_study_plan(request,subject_id,data:StudyPlanCreate):
  StudyPlanService().create_study_plan(request.user,subject_id,data)  
  return {'message':"It's being created, it's take time, please come later"}

@router.get('/all/{subject_id}',response=list[StudyPlanResponse])
def get_all_plan(request,subject_id):
  return StudyPlanService().get_all_plan_of_subject(request.user,subject_id)

@router.get('/plan/{plan_id}',response=StudyPlanResponse)
def get_plan(request,plan_id):
  return StudyPlanService().get_plan_with_is_author(request.user,plan_id)

@router.post('/plan/complete/{plan_item_id}',response=StudyPlanSessionResponse)
def complete_plan_item(request,plan_item_id,data:StudyPlanSessionCreate):
  return StudyPlanService().create_study_plan_session(request.user,plan_item_id,data)

