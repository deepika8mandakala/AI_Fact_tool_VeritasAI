from app.explanation.prompt import SYSTEM_PROMPT
from app.explanation.llm import client


def generate_explanation(
    claim: str,
    summary: dict,
    evidence: list
):

    evidence_text = ""

    reasons = []

    # ----------------------------
    # Build evidence text
    # ----------------------------

    for i, item in enumerate(evidence[:3], start=1):

        evidence_text += (
            f"Evidence {i}:\n"
            f"{item['document']['chunk_text']}\n\n"
        )

    # ----------------------------
    # Explainability
    # ----------------------------

    if evidence:

        best = evidence[0]

        if best["retrieval_score"] > 0.70:
            reasons.append("High semantic similarity")

        elif best["retrieval_score"] > 0.50:
            reasons.append("Moderate semantic similarity")

        if best["source_score"] >= 0.80:
            reasons.append("Trusted evidence source")

        elif best["source_score"] >= 0.60:
            reasons.append("Moderately trusted source")

        if best["confidence"] >= 0.90:
            reasons.append("Natural Language Inference strongly supports the verdict")

        else:
            reasons.append("Natural Language Inference confidence is moderate")

        reasons.append("Evidence directly matches the claim")

    # ----------------------------
    # Prompt
    # ----------------------------

    prompt = f"""
Claim:
{claim}

Final Verdict:
{summary['final_verdict']}

Confidence:
{summary['confidence']}

Retrieved Evidence:

{evidence_text}

Generate a concise explanation.
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
        max_tokens=250
    )

    explanation = response.choices[0].message.content

    return {
        "summary": explanation,
        "reasoning": reasons
    }