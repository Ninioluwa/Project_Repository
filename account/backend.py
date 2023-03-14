from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

Account = get_user_model()


class EmailBackend(BaseBackend):

    def authenticate(self, request, username, password, **kwargs):

        try:
            user = Account.objects.get(email=username)
            if user.check_password(password) and user.is_active:
                return user
        except:
            pass

        return None

    def get_user(self, user_id):

        return Account.objects.get(id=user_id)
