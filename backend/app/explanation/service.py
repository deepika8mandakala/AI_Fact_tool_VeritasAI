from app.explanation.prompt import SYSTEM_PROMPT
from app.explanation.llm import client


def generate_explanation(
    claim: str,
    summary: dict,
    evidence: list
):

    evidence_text = ""

    for i, item in enumerate(evidence[:3], start=1):

        evidence_text += (
            f"Evidence {i}:\n"
            f"{item['document']['chunk_text']}\n\n"
        )

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

    return response.choices[0].message.content