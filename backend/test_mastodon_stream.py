from app.social.mastodon_stream import stream_hashtag
from app.social.post_extractor import extract_post
from app.social.service import extract_claims
from app.verification.pipeline import verify_pipeline


def handle_post(post):

    print("\n")
    print("=" * 80)
    print("NEW LIVE MASTODON POST")
    print("=" * 80)

    # -------------------------
    # Extract post
    # -------------------------

    extracted = extract_post(post)

    text = extracted["text"].strip()

    print("POST URL:")
    print(extracted["url"])

    print("\nPOST TEXT:")
    print(text)

    if not text:
        print("No text. Skipping.")
        return

    # -------------------------
    # Extract claims
    # -------------------------

    claims = extract_claims(text)

    print("\nCLAIMS FOUND:", len(claims))

    if not claims:
        print("No factual-looking claims found.")
        return

    # -------------------------
    # Verify claims
    # -------------------------

    for claim in claims:

        print("\n")
        print("-" * 80)
        print("LIVE CLAIM:")
        print(claim)
        print("-" * 80)

        try:

            result = verify_pipeline(
                claim
            )

            summary = result["summary"]

            print("\nVERDICT:")
            print(
                summary["final_verdict"]
            )

            print("\nCONFIDENCE:")
            print(
                summary["confidence"]
            )

            print("\nEXPLANATION:")
            print(
                result["explanation"]
            )

        except Exception as e:

            print(
                "\nVERIFICATION ERROR:",
                type(e).__name__,
                str(e)
            )

    print("=" * 80)


print("Starting VeritasAI live verification...")
print("Hashtag: science")
print("Press CTRL+C to stop.")

stream_hashtag(
    "science",
    handle_post
)