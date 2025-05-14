# Convert Python objects to JSON and vice versa
# so it can be sent via API

from rest_framework import serializers
from .models import Company, CompanyAspectSentiment, RawTweet


""" 
TODO: 
- Return how many tweets belong to each company
- How many users follow the company

"""


# Test API to get all tweets
class RawTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawTweet
        fields = ["id", "text", "date"]


class CompanySerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(source="followers.count", read_only=True)
    # tweet_count = serializers.IntegerField(source='tweets.count', read_only=True)

    class Meta:
        model = Company
        fields = ["id", "name", "follower_count"]


# Return sentiment of an aspect of multiple companies
# Return sentiment of an aspect of a single company
class CompanyAspectSentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAspectSentiment
        fields = (
            "id",
            "tweet",
            "company",
            "aspect",
            "date",
            "sentiment",
            "sentiment_type",
        )
