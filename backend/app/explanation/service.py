from app.explanation.prompt import SYSTEM_PROMPT
from app.explanation.llm import client


def generate_explanation(
    claim: str,
    summary: dict,
    evidence: list
):
    """
    Generate a natural-language explanation for a verification result.

    The actual verification decision is produced by the verification
    pipeline. Groq is used only to explain that result.
    """

    # =====================================================
    # No Evidence
    # =====================================================

    if not evidence:

        return {
            "summary": (
                "There is insufficient evidence to verify this claim."
            ),
            "reasoning": [
                "No relevant evidence was retrieved."
            ]
        }

    # =====================================================
    # Sort Evidence
    # =====================================================

    evidence = sorted(
        evidence,
        key=lambda x: (
            x.get("relevance_score", 0),
            x.get("rerank_score", 0),
            x.get("confidence", 0)
        ),
        reverse=True
    )

    # =====================================================
    # Build Evidence Text
    # =====================================================

    evidence_text = ""

    for i, item in enumerate(
        evidence[:3],
        start=1
    ):

        document = item.get(
            "document",
            {}
        )

        evidence_text += (
            f"Evidence {i}\n"
            f"Title: {document.get('title', 'Unknown')}\n"
            f"Source: {document.get('source', 'Unknown')}\n"
            f"Text: {document.get('chunk_text', '')}\n\n"
        )

    # =====================================================
    # Best Evidence
    # =====================================================

    best = evidence[0]

    reasoning = []

    relevance_score = best.get(
        "relevance_score",
        0
    )

    source_score = best.get(
        "source_score",
        0
    )

    confidence = best.get(
        "confidence",
        0
    )

    # =====================================================
    # Reasoning
    # =====================================================

    if relevance_score > 2:

        reasoning.append(
            "Highly relevant evidence retrieved."
        )

    elif relevance_score > 1:

        reasoning.append(
            "Moderately relevant evidence retrieved."
        )

    if source_score >= 0.8:

        reasoning.append(
            "Evidence comes from a trusted source."
        )

    if confidence >= 0.9:

        reasoning.append(
            "Verification model has high confidence."
        )

    elif confidence >= 0.7:

        reasoning.append(
            "Verification model has moderate confidence."
        )

    # =====================================================
    # Verification Prompt
    # =====================================================

    prompt = f"""
Claim:
{claim}

Final Verdict:
{summary.get("final_verdict", "INSUFFICIENT_EVIDENCE")}

Confidence:
{summary.get("confidence", 0.0)}

Evidence:
{evidence_text}

Explain in 3-5 sentences why this verdict was reached.

Important:
- Use only the supplied evidence.
- Do not introduce unsupported facts.
- Do not change the final verdict.
- Clearly explain the relationship between the claim and evidence.
"""

    # =====================================================
    # Groq Explanation
    # =====================================================

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=200
        )

        explanation = (
            response
            .choices[0]
            .message
            .content
        )

        if not explanation:

            raise ValueError(
                "Groq returned an empty explanation."
            )

        return {
            "summary": explanation.strip(),
            "reasoning": reasoning
        }

    # =====================================================
    # Groq Failure Fallback
    # =====================================================

    except Exception as exc:

        print(
            "\nEXPLANATION MODEL ERROR:"
        )

        print(
            type(exc).__name__,
            str(exc)
        )

        verdict = summary.get(
            "final_verdict",
            "INSUFFICIENT_EVIDENCE"
        )

        confidence = float(
            summary.get(
                "confidence",
                0.0
            )
        )

        # ---------------------------------------------
        # Local fallback explanation
        # ---------------------------------------------

        if verdict == "SUPPORTED":

            fallback = (
                "The claim is supported by the retrieved "
                "evidence. The verification model found "
                f"supporting evidence with {confidence:.1%} "
                "confidence."
            )

        elif verdict == "CONTRADICTED":

            fallback = (
                "The claim is contradicted by the retrieved "
                "evidence. The verification model found "
                f"contradicting evidence with {confidence:.1%} "
                "confidence."
            )

        else:

            fallback = (
                "There is insufficient evidence to verify "
                "this claim. The retrieved information was "
                "not sufficient to establish reliable "
                "support or contradiction."
            )

        reasoning.append(
            "Explanation model was unavailable; "
            "a local fallback explanation was used."
        )

        return {
            "summary": fallback,
            "reasoning": reasoning
        }