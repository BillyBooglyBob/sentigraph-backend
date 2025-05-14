from rest_framework.exceptions import PermissionDenied
from useraccount.models import User


def get_user_by_email(email):
    """Fetch user by email."""
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def check_permissions(request, user_email=None):
    """Check if the requesting user has permissions to access the data."""
    if (
        request.user.email != user_email
        and not request.user.is_staff
        and not request.user.is_superuser
    ):
        raise PermissionDenied("You do not have permission to access this user's data.")
