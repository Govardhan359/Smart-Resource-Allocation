import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def parse_field_report(text: str) -> list[dict]:
    prompt = f"""You are a disaster relief coordinator AI. Analyze this field report and extract all distinct needs/problems mentioned.

Field Report:
\"\"\"{text}\"\"\"

Return ONLY a valid JSON array (no markdown, no explanation) where each object has:
- "title": short need title (max 10 words)
- "description": detailed description of the need
- "category": one of ["medical", "food", "shelter", "rescue", "logistics", "other"]
- "urgency_score": integer 1-10 (10 = most urgent)
- "area_name": location/area mentioned or "Unknown"

Example output:
[
  {{
    "title": "Medical aid needed at Sector 4",
    "description": "Three injured people need immediate medical attention near the flood zone.",
    "category": "medical",
    "urgency_score": 9,
    "area_name": "Sector 4"
  }}
]"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    needs = json.loads(raw)
    return needs if isinstance(needs, list) else []