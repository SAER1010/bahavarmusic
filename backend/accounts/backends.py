from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User


class PhoneOrEmailBackend(ModelBackend):
    """
    Authenticate against settings.AUTH_USER_MODEL using either:
    - phone_number
    - email
    - username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('phone_number') or kwargs.get('email')

        if not username or not password:
            return None

        # Clean username/phone
        identifier = str(username).strip()

        try:
            user = User.objects.get(
                Q(phone_number=identifier) |
                Q(email__iexact=identifier) |
                Q(username__iexact=identifier)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(
                Q(phone_number=identifier) |
                Q(email__iexact=identifier) |
                Q(username__iexact=identifier)
            ).order_by('id').first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
