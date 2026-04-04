
from ..repositories import SubjectRepository,SubjectAnalyzeRepository
from django.core.exceptions import ObjectDoesNotExist
from ninja.errors import HttpError
from apps.gemini import GeminiAPIService
from apps.utils import BasePaginationService

class SubjectService(BasePaginationService):
  def create_subject(self,user,data):
    data['user'] = user
    print(data)
    return SubjectRepository().create(**data)
  def get_subject_with_is_author(self,user,subject_id):
    try:
        subject = SubjectRepository().get(id=subject_id)
    except ObjectDoesNotExist:
        raise HttpError(404, "Subject not found")
    if subject.user_id != user.id:      
      raise HttpError(status_code=403,message="You are not allowed to view this subject")
    return subject
  def get_subject(self,user,subject_id):
    return self.get_subject_with_is_author(user,subject_id)
  def delete_subject(self,user,subject_id):
    subject = self.get_subject_with_is_author(user,subject_id)
    SubjectRepository().delete(subject)
    return True
  def update_subject(self,user,subject_id,data):
    subject = self.get_subject_with_is_author(user,subject_id)
    return SubjectRepository().update(subject,**data)
  
  def create_or_update_service_analyze(self,subject,data):
    try:
      subject_analyze = SubjectAnalyzeRepository().get_by_subject(subject)
      print("Already exist")
      SubjectAnalyzeRepository().update(subject_analyze,**data)
    except Exception as e:
      print("Creating",e)
      data['subject'] = subject
      subject_analyze = SubjectAnalyzeRepository().create(**data)
    return subject_analyze
  
  def update_subject_analyzing_status(self,subject,status=True,failed=False):
    # As we using background task we need this field to show to the user either done or running
    SubjectRepository().update(subject,is_analyzing=status,is_failed_analyze=failed)
  def create_quiz_for_subject(self,user,subject_id):
    from apps.subjects.tasks import analyze_subject_in_background
    subject = self.get_subject_with_is_author(user,subject_id)
    if not subject.files.all():
      raise HttpError(message="You must upload at least one file to analyze your subject",status_code=400)
    analyze_subject_in_background.delay(subject_id)
  

  def get_all_subject_by_pagination(self,user,page=1,page_size=20):
    subjects,count,has_next = SubjectRepository().filter_by_pagination(page=page,page_size=page_size,user=user)
    return self._build_pagination_response(subjects,count,page,page_size,has_next)