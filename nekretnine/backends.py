from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Custom authentication backend to authenticate users using their email instead of username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()  # Get the currently active user model
        try:
            # Match the email to find the user
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        # Check the password
        if user.check_password(password):
            return user
        return None
