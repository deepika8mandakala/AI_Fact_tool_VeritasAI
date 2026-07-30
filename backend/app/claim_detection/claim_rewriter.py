import os

from groq import Groq


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


SYSTEM_PROMPT = """
You are an expert fact-checking assistant.

Your task is to rewrite long or conversational sentences into ONE concise,
objective, factual claim.

Rules:

- Preserve the original meaning.
- Remove greetings and unnecessary words.
- Do NOT invent information.
- Return ONLY the rewritten claim.
"""


def rewrite_claim(sentence: str) -> str:
    """
    Rewrite a sentence into a concise factual claim.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": sentence
            }
        ]
    )

    return response.choices[0].message.content.strip()