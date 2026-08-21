import threading
from collections import deque

from app.social.mastodon_stream import stream_hashtag
from app.social.post_extractor import extract_post
from app.social.service import extract_claims
from app.verification.pipeline import verify_pipeline


# =========================================================
# Live Monitor State
# =========================================================

_monitor_thread = None

_monitor_running = False

_monitor_hashtag = None

_stop_event = None

_results = deque(
    maxlen=50
)

_seen_post_ids = set()

_lock = threading.Lock()


# =========================================================
# Process Incoming Post
# =========================================================

def _process_post(post):

    try:

        post_id = post.get(
            "id"
        )

        if not post_id:
            return

        # -------------------------------------------------
        # Avoid duplicate posts
        # -------------------------------------------------

        with _lock:

            if post_id in _seen_post_ids:

                return

            _seen_post_ids.add(
                post_id
            )

        # -------------------------------------------------
        # Extract post
        # -------------------------------------------------

        extracted = extract_post(
            post
        )

        text = extracted.get(
            "text",
            ""
        ).strip()

        if not text:

            return

        print(
            "\n" + "=" * 80
        )

        print(
            "LIVE POST RECEIVED"
        )

        print(
            "=" * 80
        )

        print(
            "POST:"
        )

        print(
            text
        )

        # -------------------------------------------------
        # Extract claims
        # -------------------------------------------------

        claims = extract_claims(
            text
        )

        print(
            "CLAIMS DETECTED:",
            len(claims)
        )

        if not claims:

            return

        # -------------------------------------------------
        # Verify claims
        # -------------------------------------------------

        for claim in claims:

            try:

                print(
                    "\nLIVE CLAIM:"
                )

                print(
                    claim
                )

                verification = verify_pipeline(
                    claim
                )

                summary = verification.get(
                    "summary",
                    {}
                )

                result = {
                    "post": extracted,

                    "claim": claim,

                    "verification": verification,

                    "verdict": summary.get(
                        "final_verdict",
                        "INSUFFICIENT_EVIDENCE"
                    ),

                    "confidence": summary.get(
                        "confidence",
                        0.0
                    ),
                }

                with _lock:

                    _results.appendleft(
                        result
                    )

                print(
                    "\nLIVE VERDICT:",
                    result["verdict"]
                )

                print(
                    "LIVE CONFIDENCE:",
                    result["confidence"]
                )

            except Exception as exc:

                print(
                    "CLAIM VERIFICATION ERROR:",
                    type(exc).__name__,
                    str(exc)
                )

    except Exception as exc:

        print(
            "LIVE POST PROCESSING ERROR:",
            type(exc).__name__,
            str(exc)
        )


# =========================================================
# Streaming Worker
# =========================================================

def _stream_worker(hashtag):

    global _monitor_running

    try:

        print(
            "\n" + "=" * 80
        )

        print(
            "STARTING VERITASAI LIVE MONITOR"
        )

        print(
            "HASHTAG:",
            hashtag
        )

        print(
            "=" * 80
        )

        stream_hashtag(
            hashtag=hashtag,
            on_post=_process_post,
            stop_event=_stop_event,
        )

    except Exception as exc:

        print(
            "LIVE STREAM ERROR:",
            type(exc).__name__,
            str(exc)
        )

    finally:

        with _lock:

            _monitor_running = False

        print(
            "VERITASAI LIVE MONITOR STOPPED"
        )


# =========================================================
# Start Monitor
# =========================================================

def start_monitor(hashtag):

    global _monitor_thread
    global _monitor_running
    global _monitor_hashtag
    global _stop_event

    hashtag = (
        hashtag
        .strip()
        .lstrip("#")
    )

    if not hashtag:

        raise ValueError(
            "Hashtag is required."
        )

    with _lock:

        if _monitor_running:

            return {
                "running": True,

                "hashtag": _monitor_hashtag,

                "message": (
                    "Live monitor is already running."
                ),
            }

        # ---------------------------------------------
        # New stop event for this session
        # ---------------------------------------------

        _stop_event = threading.Event()

        _monitor_running = True

        _monitor_hashtag = hashtag

        _results.clear()

        _seen_post_ids.clear()

    _monitor_thread = threading.Thread(
        target=_stream_worker,
        args=(hashtag,),
        daemon=True,
    )

    _monitor_thread.start()

    return {
        "running": True,

        "hashtag": hashtag,

        "message": (
            f"Live monitoring started for #{hashtag}."
        ),
    }


# =========================================================
# Stop Monitor
# =========================================================

def stop_monitor():

    global _monitor_running
    global _monitor_hashtag
    global _stop_event

    with _lock:

        if not _monitor_running:

            return {
                "running": False,

                "message": (
                    "Live monitor is not running."
                ),
            }

        # ---------------------------------------------
        # Signal WebSocket worker to stop
        # ---------------------------------------------

        if _stop_event is not None:

            _stop_event.set()

        _monitor_running = False

        hashtag = _monitor_hashtag

        _monitor_hashtag = None

    return {
        "running": False,

        "hashtag": hashtag,

        "message": (
            "Live monitor stopped."
        ),
    }


# =========================================================
# Status
# =========================================================

def get_status():

    with _lock:

        return {
            "running": _monitor_running,

            "hashtag": _monitor_hashtag,

            "posts_processed": len(
                _seen_post_ids
            ),

            "claims_detected": len(
                _results
            ),
        }


# =========================================================
# Results
# =========================================================

def get_results():

    with _lock:

        return list(
            _results
        )


# =========================================================
# Clear Results
# =========================================================

def clear_results():

    with _lock:

        _results.clear()

        _seen_post_ids.clear()

    return {
        "message": (
            "Live monitor results cleared."
        )
    }