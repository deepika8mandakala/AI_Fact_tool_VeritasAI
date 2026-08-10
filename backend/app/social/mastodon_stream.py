import os
import json
import time
import requests
import websocket


MASTODON_INSTANCE = os.getenv(
    "MASTODON_INSTANCE",
    "https://mastodon.social"
)

MASTODON_ACCESS_TOKEN = os.getenv(
    "MASTODON_ACCESS_TOKEN"
)


def get_streaming_host():

    response = requests.get(
        f"{MASTODON_INSTANCE}/api/v2/instance",
        headers={
            "Accept": "application/json",
            "User-Agent": "VeritasAI/1.0",
        },
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    streaming_url = (
        data
        .get("configuration", {})
        .get("urls", {})
        .get("streaming")
    )

    if not streaming_url:
        raise RuntimeError(
            "Mastodon streaming URL not found."
        )

    return streaming_url.rstrip("/")


def stream_hashtag(
    hashtag: str,
    on_post,
    stop_event=None,
):
    """
    Stream new Mastodon posts for a hashtag.

    stop_event:
        threading.Event used to gracefully stop
        the WebSocket connection.
    """

    if not MASTODON_ACCESS_TOKEN:

        raise RuntimeError(
            "MASTODON_ACCESS_TOKEN is not set."
        )

    hashtag = hashtag.lstrip("#").strip()

    if not hashtag:

        raise ValueError(
            "Hashtag cannot be empty."
        )

    streaming_host = get_streaming_host()

    ws_url = (
        f"{streaming_host}"
        "/api/v1/streaming"
    )

    print("=" * 80)
    print("MASTODON LIVE STREAM")
    print("Host:", streaming_host)
    print("Hashtag:", hashtag)
    print("=" * 80)

    while True:

        # -------------------------------------------------
        # Check whether the caller requested a stop
        # -------------------------------------------------

        if stop_event is not None and stop_event.is_set():

            print(
                "Stop requested before connection."
            )

            break

        ws = None

        try:

            print(
                "\nConnecting to Mastodon..."
            )

            ws = websocket.create_connection(
                ws_url,
                header=[
                    "Authorization: Bearer "
                    + MASTODON_ACCESS_TOKEN
                ],
                timeout=2,
            )

            ws.send(
                json.dumps({
                    "type": "subscribe",
                    "stream": "hashtag",
                    "tag": hashtag,
                })
            )

            print(
                "Connected successfully."
            )

            print(
                f"Waiting for new #{hashtag} posts..."
            )

            # -------------------------------------------------
            # Receive posts
            # -------------------------------------------------

            while True:

                # ---------------------------------------------
                # Stop check
                # ---------------------------------------------

                if (
                    stop_event is not None
                    and stop_event.is_set()
                ):

                    print(
                        "Stopping Mastodon WebSocket..."
                    )

                    break

                try:

                    message = ws.recv()

                except websocket.WebSocketTimeoutException:

                    # Timeout is intentional.
                    # It lets us periodically check stop_event.
                    continue

                if not message:
                    continue

                # ---------------------------------------------
                # Parse WebSocket message
                # ---------------------------------------------

                try:

                    event = json.loads(
                        message
                    )

                except json.JSONDecodeError:

                    continue

                event_type = event.get(
                    "event"
                )

                # Ignore heartbeat /
                # confirmation events.
                if event_type != "update":

                    continue

                payload = event.get(
                    "payload"
                )

                if not payload:
                    continue

                # ---------------------------------------------
                # Decode payload
                # ---------------------------------------------

                if isinstance(
                    payload,
                    str
                ):

                    try:

                        post = json.loads(
                            payload
                        )

                    except json.JSONDecodeError:

                        continue

                elif isinstance(
                    payload,
                    dict
                ):

                    post = payload

                else:

                    continue

                # ---------------------------------------------
                # Validate post
                # ---------------------------------------------

                if not isinstance(
                    post,
                    dict
                ):

                    continue

                if not post.get("id"):

                    continue

                # ---------------------------------------------
                # Process post
                # ---------------------------------------------

                try:

                    on_post(post)

                except Exception as exc:

                    print(
                        "\nPOST PROCESSING ERROR:",
                        type(exc).__name__,
                        str(exc)
                    )

                    # One bad post must never
                    # kill the live stream.
                    continue

        except KeyboardInterrupt:

            print(
                "\nStopping Mastodon stream..."
            )

            break

        except Exception as exc:

            # If stop was requested, don't reconnect.
            if (
                stop_event is not None
                and stop_event.is_set()
            ):

                break

            print(
                "\nMastodon stream disconnected:"
            )

            print(
                type(exc).__name__,
                str(exc)
            )

            print(
                "Reconnecting in 5 seconds..."
            )

            # Wait up to 5 seconds, but wake
            # immediately if stop is requested.
            if stop_event is not None:

                if stop_event.wait(5):

                    break

            else:

                time.sleep(5)

        finally:

            if ws is not None:

                try:

                    ws.close()

                except Exception:

                    pass

    print(
        "Mastodon live stream stopped."
    )