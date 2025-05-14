from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

# Load Aspect-Based Sentiment Analysis model
absa_tokenizer = AutoTokenizer.from_pretrained("yangheng/deberta-v3-base-absa-v1.1")
absa_model = AutoModelForSequenceClassification \
  .from_pretrained("yangheng/deberta-v3-base-absa-v1.1")

# Load a traditional Sentiment Analysis model
sentiment_model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=sentiment_model_path,
                          tokenizer=sentiment_model_path)

# Create the pipeline for aspect-based sentiment analysis
# - tokenizer: tokensises the text
# - model: performs the analysis
classifier = pipeline("text-classification", model=absa_model, tokenizer=absa_tokenizer)
