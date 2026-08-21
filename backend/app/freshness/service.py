from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def get_freshness_score(date_string: str) -> float:

    if not date_string:
        return 0.50

    try:

        try:
            published = parsedate_to_datetime(date_string)

        except Exception:
            published = datetime.fromisoformat(
                date_string.replace("Z", "+00:00")
            )

        if published.tzinfo is None:
            published = published.replace(
                tzinfo=timezone.utc
            )

        now = datetime.now(timezone.utc)

        days = (
            now - published
        ).days

        if days <= 1:
            return 1.00

        if days <= 7:
            return 0.95

        if days <= 30:
            return 0.90

        if days <= 90:
            return 0.80

        if days <= 180:
            return 0.70

        if days <= 365:
            return 0.60

        return 0.50

    except Exception:

        return 0.50