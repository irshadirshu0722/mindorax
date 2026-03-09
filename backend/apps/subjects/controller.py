from ninja import Router
from .schemas import SubjectCreate
from services import SubjectService
router = Router()

# Create subject without filles
@router.post('create-subject')
def create_subject(request, data: SubjectCreate):
  try:
    subject = SubjectService.create_subject(data)
    return 
  except:
    