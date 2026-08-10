from app.explanation.prompt import SYSTEM_PROMPT
from app.explanation.llm import client


def generate_explanation(
    claim: str,
    summary: dict,
    evidence: list
):

    if not evidence:
        return {
            "summary": "There is insufficient evidence to verify this claim.",
            "reasoning": ["No relevant evidence was retrieved."]
        }

    # -----------------------------
    # Sort evidence by quality
    # -----------------------------

    evidence = sorted(
        evidence,
        key=lambda x: (
            x.get("relevance_score", 0),
            x.get("rerank_score", 0),
            x.get("confidence", 0)
        ),
        reverse=True
    )

    evidence_text = ""

    for i, item in enumerate(evidence[:3], start=1):

        evidence_text += (
            f"Evidence {i}\n"
            f"Title: {item['document']['title']}\n"
            f"Source: {item['document']['source']}\n"
            f"Text: {item['document']['chunk_text']}\n\n"
        )

    best = evidence[0]

    reasoning = []

    if best.get("relevance_score", 0) > 2:
        reasoning.append("Highly relevant evidence retrieved.")
    elif best.get("relevance_score", 0) > 1:
        reasoning.append("Moderately relevant evidence retrieved.")

    if best.get("source_score", 0) >= 0.8:
        reasoning.append("Evidence comes from a trusted source.")

    if best.get("confidence", 0) >= 0.9:
        reasoning.append("Verification model has high confidence.")
    elif best.get("confidence", 0) >= 0.7:
        reasoning.append("Verification model has moderate confidence.")

    prompt = f"""
Claim:
{claim}

Final Verdict:
{summary['final_verdict']}

Confidence:
{summary['confidence']}

Evidence:
{evidence_text}

Explain in 3-5 sentences why this verdict was reached.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
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

    explanation = response.choices[0].message.content

    return {
        "summary": explanation,
        "reasoning": reasoning
    }