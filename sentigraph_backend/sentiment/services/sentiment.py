from datetime import datetime
from ..util.date.date import generate_date_range
from ..models import RawTweet, CompanyAspectSentiment
from .helpers import (
    ensure_company,
    ensure_aspect,
    ensure_company_aspect_sentiment,
)


def get_company_aspect_sentiment_data(aspect_name, timeframe, company_names):
    """
    Get sentiment data for a specific aspect and a list of companies over a specified timeframe.
    Params:
        aspect (str): The aspect to analyze.
        timeframe (str): The timeframe for the analysis.
        company_names (list): List of company names to analyze.
    Returns:
        dict: A dictionary containing the aspect, company names, count of days, and sentiment data.
    """
    date_range = generate_date_range(timeframe)
    tweets = RawTweet.objects.all()
    result = {}

    for company_name in company_names:
        company_obj = ensure_company(company_name, tweets)
        aspect_obj = ensure_aspect(aspect_name)
        ensure_company_aspect_sentiment(company_obj, aspect_name)
        result[company_name] = get_daily_sentiment(company_obj, aspect_obj, date_range)

    # Format response
    return {
        "aspect": aspect_name,
        "companies": company_names,
        "count": len(date_range),
        "data": [
            {
                "date": date,
                **{
                    company_name: result[company_name][i]
                    for company_name in company_names
                },
            }
            for i, date in enumerate(date_range)
        ],
    }


def get_daily_sentiment(company_obj, aspect_obj, date_range):
    """
    Get daily sentiment for a specific company and aspect over a specified date range.
    """
    result = []
    for date in date_range:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()

        sentiments = CompanyAspectSentiment.objects.filter(
            company=company_obj,
            aspect=aspect_obj,
        )
        sentiments = [s for s in sentiments if s.date.date() == target_date]

        # No sentiment data for the date
        # Append 0.0 to signify no sentiment
        if not sentiments:
            result.append(0.0)
            continue

        score = 0.0
        for s in sentiments:
            if s.sentiment_label == "Positive":
                score += s.sentiment_score
            elif s.sentiment_label == "Negative":
                score -= s.sentiment_score
        result.append(score / len(sentiments))
    return result
