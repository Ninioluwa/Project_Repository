from django.test import TestCase
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from account.models import Institution, Account
from .models import Department, Tag, Project


class TestProjectRepository(TestCase):

    def setUp(self):
        institution = Institution.objects.create(name="University of ABC")
        self.account_details = {
            "username": "test",
            "password": "testpass$123",
            "first_name": "test",
            "last_name": "user",
            "institution": institution,
            "email": "test@email.com"
        }
        self.account = Account.objects.create_user(
            **self.account_details
        )
        self.tag = Tag.objects.create(name="Test")
        self.client.force_login(user=self.account)

    def test_create_department(self):
        department = Department.objects.create(name="Computer Science")
        self.assertIsNotNone(department.id)
        self.assertEqual(department.name, "Computer Science")
        self.assertEqual(str(department), "Computer Science")

    def test_create_tag(self):
        tag = Tag.objects.create(name="AI")
        self.assertIsNotNone(tag.id)
        self.assertEqual(tag.name, "AI")
        self.assertEqual(str(tag), "AI")

    def test_create_project(self):
        path = reverse_lazy("project-create")
        coverpage = open("/home/toluhunter/Pictures/lamp.jpeg", "rb")
        document = open(
            "/home/toluhunter/Downloads/Open Source Documentation Group 7.pdf", "rb")
        files = {
            "cover_page": coverpage,
            "document": document
        }

        institution = Institution.objects.create(name="University of XYZ")
        department = Department.objects.create(name="Software Engineering")

        data = {
            "title": "Test Project",
            "institution": institution.id,
            "department": department.id,
            "scholar": self.account.id,
            "description": "A test project description.",
            "url": "https://example.com/test-project",
            "tags": self.tag.id,
            "cover_page": SimpleUploadedFile("test.jpeg", coverpage.read()),
            "document": SimpleUploadedFile("test.pdf", document.read()),
            "supervisor": "John Doe",
            "year_published": "2022",
        }

        res = self.client.post(path, data=data)

        document.close()
        coverpage.close()

        self.assertEquals(302, res.status_code)

        project = Project.objects.last()

        self.assertIsNotNone(project.id)
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.institution, institution)
        self.assertEqual(project.department, department)
        self.assertEqual(project.scholar, self.account)
        self.assertEqual(project.description, "A test project description.")
        self.assertIsNotNone(project.cover_page)
        self.assertIsNotNone(project.document)
        self.assertEqual(project.url, "https://example.com/test-project")
        self.assertEqual(project.supervisor, "John Doe")
        self.assertEqual(project.year_published, "2022")
        self.assertEqual(str(project), "Test Project")
