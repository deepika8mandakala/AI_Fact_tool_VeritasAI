import os
import requests


MASTODON_INSTANCE = os.getenv(
    "MASTODON_INSTANCE",
    "https://mastodon.social"
)

MASTODON_ACCESS_TOKEN = os.getenv(
    "MASTODON_ACCESS_TOKEN"
)


def _headers():

    headers = {
        "Accept": "application/json",
        "User-Agent": "VeritasAI/1.0",
    }

    if MASTODON_ACCESS_TOKEN:
        headers["Authorization"] = (
            f"Bearer {MASTODON_ACCESS_TOKEN}"
        )

    return headers


def get_public_posts(limit: int = 5):

    url = (
        f"{MASTODON_INSTANCE}"
        "/api/v1/timelines/public"
    )

    response = requests.get(
        url,
        params={
            "limit": limit
        },
        headers=_headers(),
        timeout=15,
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"Mastodon public timeline failed. "
            f"HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    return response.json()


def get_hashtag_posts(
    hashtag: str,
    limit: int = 5
):

    hashtag = hashtag.lstrip("#")

    url = (
        f"{MASTODON_INSTANCE}"
        f"/api/v1/timelines/tag/{hashtag}"
    )

    response = requests.get(
        url,
        params={
            "limit": limit
        },
        headers=_headers(),
        timeout=15,
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"Mastodon hashtag timeline failed. "
            f"HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    return response.json()