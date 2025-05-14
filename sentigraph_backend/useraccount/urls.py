from django.urls import path

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenRefreshView
from . import api

urlpatterns = [
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path(
        "user/<str:email>/companies/<uuid:company_id>/",
        api.remove_company_from_user,
        name="rest_remove_user_company",
    ),
    path(
        "user/<str:email>/companies/<str:company_name>/",
        api.add_company_to_user,
        name="rest_add_user_company",
    ),
    path(
        "user/<str:email>/companies/",
        api.get_user_companies,
        name="rest_user_companies",
    ),
    path("user/<str:email>/", api.get_user_information, name="rest_user_details"),
]
