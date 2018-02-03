from django.conf import settings
from django.contrib.auth.models import check_password
from .models import User

class EmailAuthBackend(object):
    def authenticate(self, email=None, password=None):
        try:
            profile = User.objects.get(email=email)
            if profile.check_password(password):
                return profile
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            profile = User.objects.get(pk=user_id)
            if profile.is_active:
                return profile
            return None
        except User.DoesNotExist:
            return None