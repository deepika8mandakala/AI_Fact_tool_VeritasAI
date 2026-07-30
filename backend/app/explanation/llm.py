import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)