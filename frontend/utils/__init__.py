import requests


API_URL = "http://127.0.0.1:8000"


# =========================================================
# Normal Claim Verification
# =========================================================

def verify_claim(
    claim,
    top_k=5
):

    payload = {
        "claim": claim,
        "top_k": top_k
    }

    response = requests.post(
        f"{API_URL}/verification/verify",
        json=payload,
        timeout=60,
    )

    print(
        "Status Code:",
        response.status_code
    )

    print(
        "Response Text:"
    )

    print(
        response.text
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Social Media Post Verification
# =========================================================

def verify_social_post(url):

    payload = {
        "url": url
    }

    response = requests.post(
        f"{API_URL}/verification/social/verify",
        json=payload,
        timeout=120,
    )

    print(
        "Social Verification Status:",
        response.status_code
    )

    print(
        "Social Verification Response:"
    )

    print(
        response.text
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Analytics
# =========================================================

def get_history():

    response = requests.get(
        f"{API_URL}/analytics/history",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_stats():

    response = requests.get(
        f"{API_URL}/analytics/stats",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def clear_history():

    response = requests.delete(
        f"{API_URL}/analytics/history",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Batch Verification
# =========================================================
# Kept here for backend compatibility.
# The Streamlit UI no longer uses batch verification.

def verify_batch(
    claims,
    top_k=5
):

    payload = {
        "claims": claims,
        "top_k": top_k
    }

    response = requests.post(
        f"{API_URL}/verification/verify-batch",
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# LIVE MONITOR
# =========================================================

def start_live_monitor(
    hashtag
):

    response = requests.post(
        f"{API_URL}/social/live/start",
        json={
            "hashtag": hashtag
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def stop_live_monitor():

    response = requests.post(
        f"{API_URL}/social/live/stop",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_live_status():

    response = requests.get(
        f"{API_URL}/social/live/status",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_live_results():

    response = requests.get(
        f"{API_URL}/social/live/results",
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "results",
        []
    )


def clear_live_results():

    response = requests.delete(
        f"{API_URL}/social/live/results",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()