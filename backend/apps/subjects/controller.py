from ninja import Router
from .schemas import SubjectCreate,SubjectResponse
from .services import SubjectService
from apps.permissions import IsAuthenticated

router = Router(auth=IsAuthenticated())
# Create subject without filles
@router.post('/create-subject',response=SubjectResponse)
def create_subject(request, data: SubjectCreate):
  subject = SubjectService().create_subject(request.user,data.model_dump())
  return subject

@router.get('/get-subject/{subject_id}',response=SubjectResponse)
def get_subject(request,subject_id:int):
  return SubjectService().get_subject(request.user,subject_id)

@router.delete('/delete-subject/{subject_id}')
def delete_subject(request,subject_id):
  SubjectService().delete_subject(request.user,subject_id)
  return {'message':'Successfully deleted the subject'}

@router.put('/update-subject/{subject_id}',response=SubjectResponse)
def update_subject(request,subject_id,data:SubjectCreate):
  return SubjectService().update_subject(request.user,subject_id,data.model_dump())