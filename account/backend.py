from django.contrib.auth.backends import BaseBackend
from .models import Account

class EmailBackend(BaseBackend):

    def authenticate(self, request, username, password, **kwargs):
        
        try:
            user = Account.objects.get(email=username)
            if user.check_password(password) and user.is_active:
                return user
        except:
            pass

        return None