# Get the date range from the request
# - timeframe is a string in the format "90d"
from datetime import datetime, timedelta


def parse_date_range(timeframe: str) -> list[datetime.date]:
    """
    Parse the date range from the given timeframe string.
    Params:
      - timeframe is expected to be a string in the format "90d",
      where "90" is the number of days.
    Returns:
      - a tuple of start_date and end_date.
    """
    end_date = datetime.strptime("2009-06-22", "%Y-%m-%d").date()

    days = int(timeframe[:-1])  # Extract the number of days from the timeframe
    start_date = end_date - timedelta(days=days)

    return start_date, end_date


# Generate a list of dates between start_date and end_date
def generate_date_range(timeframe: str) -> list[str]:
    """
    Generate a list of dates between start_date and end_date based on the given timeframe.
    Params:
      - timeframe is expected to be a string in the format "90d",
      where "90" is the number of days.
    Returns:
      - A list of dates between start_date and end_date in ISO format.
    """
    start_date, end_date = parse_date_range(timeframe)

    delta = (end_date - start_date).days
    return [(start_date + timedelta(days=i)).isoformat() for i in range(delta + 1)]
