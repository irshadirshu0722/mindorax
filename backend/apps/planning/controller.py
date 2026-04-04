
from ninja import Router,Query
from .schemas import StudyPlanCreate,StudyPlanResponse,StudyPlanSessionCreate,StudyPlanSessionResponse,StudyPlanShortResponse
from .services import StudyPlanService
from apps.permissions import IsAuthenticated
from apps.utils import PaginationResponse
"""
1 - Create Plan
2 - All Plan listing
3 - get a plan
4 - complete one task in a plan
"""

router = Router(auth=IsAuthenticated())

@router.post("/create/{subject_id}")
def create_study_plan(request,subject_id,data:StudyPlanCreate):
  StudyPlanService().create_study_plan(request.user,subject_id,data.dict())  
  return {'message':"It's being created, it's take time, please come later"}

@router.get('/all/{subject_id}',response=PaginationResponse[StudyPlanShortResponse])
def get_all_plan(request,subject_id,page:int=Query(1),page_size:int=Query(20)):
  return StudyPlanService().get_all_plan_with_pagination(request.user,subject_id,page,page_size)

@router.get('/plan/{plan_id}',response=StudyPlanResponse)
def get_plan(request,plan_id):
  return StudyPlanService().get_plan_with_is_author(request.user,plan_id)

@router.post('/plan/complete/{plan_item_id}',response=StudyPlanSessionResponse)
def complete_plan_item(request,plan_item_id,data:StudyPlanSessionCreate):
  return StudyPlanService().create_study_plan_session(request.user,plan_item_id,data.dict())

