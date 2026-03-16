from django.test import Client, TestCase

from apps.subjects.models import Subject
from apps.users.models import User
from apps.users.services.token_service import TokenService


class SubjectCreateApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="subject-owner@example.com",
            password="testpass123",
            oauth_provider="google",
            oauth_id="google-user-1",
        )
        self.client.cookies["access_token"] = TokenService.create_access_token(self.user.id)

    def test_create_subject_creates_record_for_authenticated_user(self):
        payload = {
            "title": "Backend System Design",
            "description": "Study API architecture and database design.",
            "goal": "Build a complete backend project by the end of the month.",
            "deadline": "2026-04-15",
            "status": "active",
        }

        response = self.client.post(
            "/api/subject/create",
            data=payload,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        subject = Subject.objects.get()
        self.assertEqual(subject.user, self.user)
        self.assertEqual(subject.title, payload["title"])
        self.assertEqual(subject.description, payload["description"])
        self.assertEqual(subject.goal, payload["goal"])
        self.assertEqual(str(subject.deadline), payload["deadline"])
        self.assertEqual(subject.status, payload["status"])

        data = response.json()
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["description"], payload["description"])
        self.assertEqual(data["goal"], payload["goal"])
        self.assertEqual(data["deadline"], payload["deadline"])
        self.assertEqual(data["status"], payload["status"])
        self.assertEqual(data["files"], [])
