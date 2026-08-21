def calculate_quality_score(
    retrieval: float,
    rerank: float,
    source: float,
    freshness: float
):
    """
    Calculate overall evidence quality score.
    Returns:
        quality_score (0-100)
        quality_label
        stars
    """

    score = (
        retrieval * 0.30 +
        rerank * 0.35 +
        source * 0.20 +
        freshness * 0.15
    )

    score *= 100

    if score >= 90:
        label = "Excellent"
        stars = 5

    elif score >= 80:
        label = "Very Good"
        stars = 4

    elif score >= 70:
        label = "Good"
        stars = 3

    elif score >= 60:
        label = "Fair"
        stars = 2

    else:
        label = "Weak"
        stars = 1

    return {
        "quality_score": round(score, 1),
        "quality_label": label,
        "stars": stars
    }