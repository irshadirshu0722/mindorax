
from ..repositories import SubjectRepository
from django.core.exceptions import ObjectDoesNotExist
from ninja.errors import HttpError

class SubjectService:
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