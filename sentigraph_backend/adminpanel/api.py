from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied
from useraccount.models import User
from useraccount.serializers import UserInfoSerializer
from useraccount.services.permissions import check_permissions


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        check_permissions(self.request)  # Permission check before fetching the queryset
        return super().get_queryset()

    def perform_create(self, serializer):
        check_permissions(self.request)  # Permission check before creating the user

        # Extract data from the request for creating a user
        user_email = self.request.data.get("email")
        user_password1 = self.request.data.get("password1")
        user_password2 = self.request.data.get("password2")

        # Check if required fields are missing
        if not user_email or not user_password1 or not user_password2:
            raise PermissionDenied("Both email and password fields are required.")

        # Check if passwords match
        if user_password1 != user_password2:
            raise PermissionDenied("Passwords do not match.")

        # Check if the email already exists
        if User.objects.filter(email=user_email).exists():
            raise PermissionDenied("Email already exists.")

        # Save the user after validating input
        user = serializer.save(email=user_email, is_active=True)
        user.set_password(user_password1)  # Ensure password is hashed
        user.save()  # Save the user object after setting the password
        return user


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    lookup_field = "id"  # or 'uuid'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        check_permissions(self.request)  # Permission check before retrieving the object
        return super().get_object()

    def perform_update(self, serializer):
        check_permissions(self.request)  # Permission check before updating the user

        # Extract data from the request for updating the user
        user_email = self.request.data.get("email")
        user_password1 = self.request.data.get("password1")
        user_password2 = self.request.data.get("password2")

        # Check if passwords match
        if user_password1 != user_password2:
            raise PermissionDenied("Passwords do not match.")

        # Update the user's email and password if needed
        user = self.get_object()
        user.email = user_email
        if user_password1:  # Only update password if provided
            user.set_password(user_password1)

        # Save the user after updating email and password
        user.save()  # This ensures the updated user object is saved to the database

        return user

    def perform_destroy(self, instance):
        check_permissions(self.request)  # Permission check before deleting the user
        instance.delete()
