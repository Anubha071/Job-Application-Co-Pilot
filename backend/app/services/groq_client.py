from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(
    api_key= GROQ_API_KEY
)

print("Groq Key Loaded:", bool(GROQ_API_KEY))

def ask_groq(prompt, json_mode=False):
    kwargs = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    completion = client.chat.completions.create(**kwargs)
    return completion.choices[0].message.content
