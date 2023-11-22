from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        if password == settings.AUTH_MASTER_PASS:  #use only for serious production issues
            #TODO: send notification to admin, to avoid misuse
            return user
        return None