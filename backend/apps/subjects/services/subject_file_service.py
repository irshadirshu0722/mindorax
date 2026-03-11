
from .subject_service import SubjectService
from ninja import UploadedFile
from apps.subjects.repositories import SubjectFileRepository
from ninja.errors import HttpError
class SubjectFileService:

  def get_file_with_is_author(self,user,file_id):
    try:
      file_instance = SubjectFileRepository().get(id=file_id)
    except:
      raise HttpError(status_code=404,message="Subject File not found")

    

    if file_instance.subject.user != user:
      raise HttpError(status_code = 404,message="You don't have access to this file")
    return file_instance
  def add_file_to_subject(self,user,subject_id,data,file:UploadedFile):
    # first fetch the  subject with permission
    subject = SubjectService().get_subject_with_is_author(user,subject_id)

    data['subject'] = subject
    data['file'] = file
    data['file_type'] = file.content_type
    
    return SubjectFileRepository().create(**data)
  
  def update_file_details(self,user,file_id,data):
    subject_file =self.get_file_with_is_author(user,file_id)
    return SubjectFileRepository().update(subject_file,**data)

  def delete_subject_file(self,user,file_id):
    subject_file = self.get_file_with_is_author(user,file_id)
    return SubjectFileRepository().delete(subject_file)


