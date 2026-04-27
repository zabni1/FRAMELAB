from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q


class EmailAuth(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
       user_model = get_user_model()
       try:
           user = user_model.objects.get(Q(email=email, active_status=True) | Q(username=email, active_status=True))
           if user.check_password(password):
                return user
           else:
               return None
       except (user_model.DoesNotExist, get_user_model().MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None