# Tells Django which function to call
# when a request is made to a specific URL

from django.urls import path

from . import api

urlpatterns = [
    path("company/<str:company>/", api.get_company, name="get_company"),
    path(
        "sentiments/",
        api.get_aspect_company_sentiment,
        name="get_aspect_company_sentiment",
    ),
    # Test API to get all tweets
    path("tweets", api.get_raw_tweet_data, name="get_raw_tweet_data"),
]

# 1st path example call
# GET /api/company/Apple/

# 2nd path example call
# GET /api/sentiment/sentiments/?companies=Apple&companies=Tesla&aspect=sustainability&timeframe=90d
