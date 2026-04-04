from django.test import Client, TestCase

from apps.subjects.models import Subject
from apps.users.models import User
from apps.users.services.token_service import TokenService
import pytest

class SubjectTestCase(TestCase):
  def setUp(self):
      self.client = Client()

  @pytest.mark.django_db
  def test_create_subject_real(self,):

      user = User.objects.create_user(email="test@gmail.com", password="123")
      access_token = TokenService.create_access_token(user.id)
      body = {"title": "Math","description":"full maths course",'goal':"Class Test","deadline":"2026-04-04","status":"Active"}
      response = self.client.post(
          "/api/subject/create",
          data=body,
          content_type="application/json",HTTP_COOKIE=f"access_token={access_token}"
      )
      print(response.json())
      assert response.status_code == 200

      assert Subject.objects.filter(**body).exists()

    
  @pytest.mark.django_db
  def test_update_subject_success(self):
      # Create user
      user = User.objects.create_user(
          email="test@gmail.com",
          password="123"
      )

      access_token = TokenService.create_access_token(user.id)
      body = {"title": "Math","description":"full maths course",'goal':"Class Test","deadline":"2026-04-04","status":"Active"}
      # Create subject
      subject = Subject.objects.create(
          user=user,
          **body
      )
      update_body = {"title": "Math","description":"full maths course",'goal':"Class Test","deadline":"2026-04-04","status":"Active"}
      # Update request
      response = self.client.put(
          f"/api/subject/update/{subject.id}",
          data={"title": "Physics"},
          content_type="application/json",HTTP_COOKIE=f"access_token={access_token}"

      )
      print(response.text)
      assert response.status_code == 200

      subject.refresh_from_db()
      assert subject.title == "Physics"
      assert subject.description == "full maths course"