# Define what the API actually does
# - Handles incoming requests
# - Fetches data from the database using Django ORM (Models)
# - Returns data in JSON format
#   - by converting data from Python objects to JSON using serializers

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .models import Company, RawTweet
from .serializers import (
    CompanySerializer,
    RawTweetSerializer,
)
from .services.helpers import ensure_company
from .services.sentiment import get_company_aspect_sentiment_data


# Test API to get all tweets
@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_raw_tweet_data(request):
    tweets = RawTweet.objects.all()
    serializer = RawTweetSerializer(tweets, many=True)

    return JsonResponse(
        {
            "count": len(tweets),
            "data": serializer.data,
        }
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_company(request, company):
    """
    Get company information
    - If the company does not exist, create it (and save related tweets in ClassifiedTweet)
    - If the company exists, return its information
    """
    # Check if the company exists yet
    tweets = RawTweet.objects.all()

    ensure_company(company, tweets)

    # Return the company information
    company = Company.objects.get(name=company)
    serializer = CompanySerializer(company)
    return JsonResponse(
        {
            "data": serializer.data,
        }
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_aspect_company_sentiment(request):
    """
    Get sentiment for a specific aspect for a list of companies
    - aspect: the aspect to analyze
    - timeframe: the time range for the analysis (e.g. "90d")
    - companies: a list of company names
    """
    aspect_name = request.GET.get("aspect")
    timeframe = request.GET.get("timeframe")
    company_names = request.GET.getlist("companies")
    if not aspect_name or not company_names or not timeframe:
        return JsonResponse({"error": "Missing required query parameters"}, status=400)

    # Normalise the input
    aspect_name = aspect_name.lower()
    timeframe = timeframe.lower()
    company_names = [c.lower() for c in company_names]

    data = get_company_aspect_sentiment_data(aspect_name, timeframe, company_names)
    return JsonResponse(data)
