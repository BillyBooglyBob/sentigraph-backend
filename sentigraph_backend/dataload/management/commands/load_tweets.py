from django.core.management.base import BaseCommand
import kagglehub
import os
import pandas as pd
from sentiment.models import RawTweet
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = "Loads tweets from Kaggle Sentiment140 dataset into the database"

    def handle(self, *args, **options):
        # Don't load data again if it already exists
        if RawTweet.objects.exists():
            self.stdout.write("Tweets already loaded. Skipping.")
            return

        # Load and parse dataset from Kaggle
        # Step 1: Download
        dataset_path = kagglehub.dataset_download("kazanova/sentiment140")
        self.stdout.write(f"Dataset downloaded to: {dataset_path}")

        # Step 2: Find CSV
        csv_file_path = None
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".csv"):
                    csv_file_path = os.path.join(root, file)
                    break
            if csv_file_path:
                break

        if not csv_file_path:
            self.stdout.write(self.style.ERROR("CSV file not found."))
            return

        self.stdout.write(f"Loading CSV: {csv_file_path}")

        # Step 3: Load and process
        df = pd.read_csv(csv_file_path, encoding="ISO-8859-1", header=None)
        df.columns = ["target", "ids", "date", "flag", "user", "text"]
        df = df[["date", "text"]]
        df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
        df = df.dropna(subset=["date"])

        # Optional: limit for testing
        # df = df.head(1000)

        created = 0
        for _, row in df.iterrows():
            RawTweet.objects.create(text=row["text"], date=row["date"])
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded {created} tweets."))
