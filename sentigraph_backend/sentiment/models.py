from uuid import uuid4

from django.conf import settings
from django.db import models


class RawTweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateTimeField()
    text = models.TextField()


class ClassifiedTweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateTimeField()
    text = models.TextField()
    company = models.ForeignKey("Company", on_delete=models.CASCADE)


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)


class Aspect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)


class CompanyAspectSentiment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tweet = models.ForeignKey("ClassifiedTweet", on_delete=models.CASCADE)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)

    aspect = models.ForeignKey("Aspect", on_delete=models.CASCADE)
    date = models.DateTimeField()

    # Only store if dominant positive or negative
    sentiment_score = models.FloatField()  # range from 0.0 to 1.0
    sentiment_label = models.CharField(
        max_length=10,
        choices=[
            ("Neutral", "Neutral"),
            ("Positive", "Positive"),
            ("Negative", "Negative"),
        ],
        default="Neutral",
    )
