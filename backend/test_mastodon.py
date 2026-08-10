from app.social.service import verify_mastodon_posts


print("=" * 80)
print("VERITASAI SOCIAL MEDIA TEST")
print("=" * 80)
print("Fetching recent #science posts...")
print("=" * 80)

try:

    results = verify_mastodon_posts(
        limit=5
    )

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    for result in results:
        print(result)

except Exception as exc:

    print(
        "\nERROR:",
        type(exc).__name__,
        str(exc)
    )