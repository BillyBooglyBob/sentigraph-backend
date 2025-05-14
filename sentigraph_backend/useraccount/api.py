from django.http import JsonResponse
from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from useraccount.models import User
from sentiment.models import Company
from useraccount.serializers import UserInfoSerializer
from sentiment.serializers import CompanySerializer
from useraccount.services.permissions import check_permissions, get_user_by_email


# Get user information
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_information(request, email):
    # Check email is valid
    user = get_user_by_email(email)
    if not user:
        return JsonResponse(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

    # Permission check
    # Check user has permission (is the user themselves or an admin)
    try:
        check_permissions(request, user.email)
    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserInfoSerializer(user)
    return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_companies(request, email):
    # Check email is valid
    user = get_user_by_email(email)
    if not user:
        return JsonResponse(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

    # Permission check
    # Check user has permission (is the user themselves or an admin)
    try:
        check_permissions(request, user.email)
    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    # Fetch companies info by expanding the company objects
    # in the user's companies field using .all()
    companies = user.companies.all()
    companies_data = CompanySerializer(companies, many=True).data
    return JsonResponse({"data": companies_data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_company_to_user(request, email, company_name):
    # Step 1: Validate user
    user = get_user_by_email(email)
    if not user:
        return JsonResponse(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

    # Step 2: Check permission
    try:
        check_permissions(request, user.email)
    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    # Step 3: Clean input & fetch/create company
    company_name = company_name.strip().lower()
    company_obj, created = Company.objects.get_or_create(name=company_name)

    # Step 4: Check if already added
    # name__iexact is case insensitive and automatically checks the
    # name field of each company object
    if user.companies.filter(name__iexact=company_name).exists():
        return JsonResponse(
            {"error": "Company already added."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Step 5: Add
    user.companies.add(company_obj)
    return JsonResponse({"message": "Company added."}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_company_from_user(request, email, company_id):
    print("DELETE called:", email, company_id)

    # Check email is valid
    user = get_user_by_email(email)
    if not user:
        return JsonResponse(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

    # Permission check
    # Check user has permission (is the user themselves or an admin)
    try:
        check_permissions(request, user.email)
    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    # Check if the company exists
    try:
        # Yes, remove it
        company = user.companies.get(id=company_id)
        user.companies.remove(company)
        return JsonResponse({"message": "Company removed."}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        # No, return error
        return JsonResponse(
            {"error": "Company not found in user's list."},
            status=status.HTTP_404_NOT_FOUND,
        )
