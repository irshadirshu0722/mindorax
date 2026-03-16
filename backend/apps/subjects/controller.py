from ninja import Router,File,Path,Form
from ninja.files import UploadedFile
from .schemas import SubjectCreate,SubjectAnalyzeResponse,SubjectFileCreate,SubjectFileResponse,SubjectResponse
from .services import SubjectService,SubjectFileService
from apps.permissions import IsAuthenticated

router = Router(auth=IsAuthenticated(),)
# Create subject without filles
@router.post('/create',response=SubjectResponse)
def create_subject(request, data: SubjectCreate):
  subject = SubjectService().create_subject(request.user,data.model_dump())
  return subject

@router.get('/get/{subject_id}',response=SubjectResponse)
def get_subject(request,subject_id:int):
  return SubjectService().get_subject(request.user,subject_id)

@router.delete('/delete/{subject_id}')
def delete_subject(request,subject_id):
  SubjectService().delete_subject(request.user,subject_id)
  return {'message':'Successfully deleted the subject'}

@router.put('/update/{subject_id}',response=SubjectResponse)
def update_subject(request,subject_id,data:SubjectCreate):
  return SubjectService().update_subject(request.user,subject_id,data.model_dump())




# Subject File management
@router.post('/file/create/{subject_id}',response=SubjectFileResponse)
def add_file_to_subject(request,subject_id:Path[int],data:Form[SubjectFileCreate],file:File[UploadedFile]):
  subject_file = SubjectFileService().add_file_to_subject(request.user,subject_id,data.dict(),file) 
  return subject_file

@router.put('/file/update/{file_id}',response=SubjectFileResponse)
def update_file_details(request,file_id:Path[int],data:SubjectFileCreate):
  subject_file = SubjectFileService().update_file_details(request.user,file_id,data.dict())
  return subject_file

@router.delete('/file/delete/{file_id}')
def delete_subject_file(request,file_id:Path[int]):
  SubjectFileService().delete_subject_file(request.user,file_id)
  return {'message':"Subject file deleted successfully"}


# Analyse 
@router.post('/analyse/{subject_id}')
def analyse(request,subject_id:int):
  SubjectService().analyse_subject(request.user,subject_id)
  return {"message":"Subject start analyzing. You are in Free Mode So It takes time please come later"}