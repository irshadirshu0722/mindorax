
from repositories import SubjectRepository

class SubjectService:
  def create_subject(self,data):
    return SubjectRepository.create(data)
  