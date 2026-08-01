import requests

API_URL = "http://127.0.0.1:8000"


def verify_claim(claim, top_k=5):

    payload = {
        "claim": claim,
        "top_k": top_k
    }

    response = requests.post(
        f"{API_URL}/verification/verify",
        json=payload
    )

    print("Status Code:", response.status_code)
    print("Response Text:")
    print(response.text)

    response.raise_for_status()

    return response.json()


def get_history():
    response = requests.get(
        f"{API_URL}/analytics/history"
    )
    response.raise_for_status()
    return response.json()


def get_stats():
    response = requests.get(
        f"{API_URL}/analytics/stats"
    )
    response.raise_for_status()
    return response.json()


def clear_history():
    response = requests.delete(
        f"{API_URL}/analytics/history"
    )
    response.raise_for_status()
    return response.json()
def verify_batch(claims, top_k=5):

    payload = {
        "claims": claims,
        "top_k": top_k
    }

    response = requests.post(
        f"{API_URL}/verification/verify-batch",
        json=payload
    )

    response.raise_for_status()

    return response.json()