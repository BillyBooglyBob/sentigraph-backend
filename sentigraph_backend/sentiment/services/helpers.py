from time import clock_getres
from ..models import Company, Aspect, ClassifiedTweet, CompanyAspectSentiment
from ..util.sentiment_analysis.sentiment_analysis import get_sentiment_for_aspect
import re


def ensure_company(company_name, tweets):
    """
    Ensure that a company exists in the database.
    If it does not exist, create it and save all tweets related to the company.
    """
    company_obj = Company.objects.get_or_create(
        name__iexact=company_name, defaults={"name": company_name}
    )
    if not ClassifiedTweet.objects.filter(company=company_obj).exists():
        print(f"Created company: {company_name}, now scanning tweets...")
        for tweet in tweets:
            if re.search(
                r"\b" + re.escape(company_name) + r"\b", tweet.text, re.IGNORECASE
            ):
                print("Found tweet for company:", company_name, ":", tweet.text)
                ClassifiedTweet.objects.create(
                    date=tweet.date, text=tweet.text, company=company_obj
                )
    print("Company object created:", company_obj)
    return company_obj


def ensure_aspect(aspect_name):
    """
    Ensure that an aspect exists in the database.
    If it does not exist, create it.
    """
    aspect_obj, _ = Aspect.objects.get_or_create(name=aspect_name)
    return aspect_obj


def ensure_company_aspect_sentiment(company_obj, aspect_name):
    """
    Ensure that the sentiment for a company and aspect is calculated.
    If it does not exist, calculate and save it.
    """
    aspect_obj = Aspect.objects.get(name=aspect_name)

    if not CompanyAspectSentiment.objects.filter(
        company=company_obj, aspect=aspect_obj
    ).exists():
        print("Sentiment for company and aspect not calculated yet.")

        company_tweets = ClassifiedTweet.objects.filter(company=company_obj)
        print("Company tweets:", company_tweets, "for company:", company_obj)
        for tweet in company_tweets:
            result = get_sentiment_for_aspect(tweet.text, aspect_name)
            print(
                f"Sentiment for tweet '{tweet.text}' for aspect '{aspect_name}': {result}"
            )
            CompanyAspectSentiment.objects.create(
                tweet=tweet,
                company=company_obj,
                aspect=aspect_obj,
                date=tweet.date,
                sentiment_label=result["label"],
                sentiment_score=result["score"],
            )
