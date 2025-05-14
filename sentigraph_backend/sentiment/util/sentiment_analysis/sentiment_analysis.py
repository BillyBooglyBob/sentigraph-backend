from .sentiment_model import classifier, sentiment_model


def get_sentiment_for_aspect(text, aspect):
    """
    Perform sentiment analysis on the given text and aspect.
    """
    output = classifier(text, text_pair=aspect)[0]
    return {"label": output["label"], "score": output["score"]}


def get_overall_sentiment(text):
    """
    Perform overall sentiment analysis on the given text.
    """
    sentiment = sentiment_model([text])[0]
    return {"label": sentiment["label"], "score": sentiment["score"]}
