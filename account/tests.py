from uuid import uuid4

from django.test import TestCase
from django.urls import reverse_lazy
from account.models import Account, Institution


class TestAccountFeatures(TestCase):
    def setUp(self) -> None:
        self.institute = Institution.objects.create(
            name="TestUni"
        )
        self.account_details = {
            "username": "test",
            "password": "testpass$123",
            "first_name": "test",
            "last_name": "user",
            "institution": self.institute,
            "email": "test@email.com"
        }
        self.account = Account.objects.create_user(
            **self.account_details
        )
        self.client.force_login(user=self.account)

    def test_templates_used(self):
        login_path = reverse_lazy("login")
        logout_path = reverse_lazy("logout")
        profile_path = reverse_lazy(
            "account-profile", kwargs={"id": self.account.id})
        register_path = reverse_lazy("register")
        edit_profile_path = reverse_lazy("edit-profile")

        res = self.client.get(register_path)
        self.assertTemplateUsed(res, "registration/register.html")

        res = self.client.get(login_path)
        self.assertTemplateUsed(res, "registration/login.html")

        res = self.client.get(profile_path)
        self.assertTemplateUsed(res, "viewprofile.html")

        res = self.client.get(logout_path)
        self.assertTemplateUsed(res, "logout.html")

        res = self.client.get(edit_profile_path)
        self.assertTemplateUsed(res, "updateprofile.html")

    def test_fetch_details(self):
        path = reverse_lazy("account-profile", kwargs={"id": self.account.id})

        res = self.client.get(path)

        # test details returned for valid account
        self.assertEquals(200, res.status_code)

    def test_invalid_account_profile(self):
        path = reverse_lazy("account-profile", kwargs={"id": uuid4()})

        res = self.client.get(path)

        # test details returned for valid account
        self.assertEquals(404, res.status_code)

    def test_login(self):
        self.client.logout()
        path = reverse_lazy("login")

        res = self.client.post(path, data={
            "username": self.account_details["username"],
            "password": self.account_details["password"]
        })

        self.assertEquals(302, res.status_code)

        # Test invalid login details does not return 302
        res = self.client.post(path, data={
            "username": "fakeuser",
            "password": "fakepass"
        })

        self.assertNotEquals(302, res.status_code)

    def test_register(self):

        path = reverse_lazy("register")

        account_details = {
            "username": "ini",
            "password": "ini$ecretPa$$",
            "c_password": "ini$ecretPa$$",
            "first_name": "inioluwa",
            "last_name": "tunde",
            "institution": self.institute.id,
            "email": "ini@email.com"
        }

        res = self.client.post(path, data=account_details)
        self.assertEquals(302, res.status_code)
