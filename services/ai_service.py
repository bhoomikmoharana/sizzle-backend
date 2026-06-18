import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_recipes(ingredients: list[str]):
    ingredients_text = ", ".join(ingredients)

    prompt = f"""
You are an expert chef for a cooking app called Sizzle AI.

User ingredients:
{ingredients_text}

Suggest 3 dishes.

Rules:
- Return ONLY valid JSON.
- No markdown.
- Give detailed cooking instructions.
- Each step should be 1-3 sentences long.
- ingredients_used must not contain duplicates.
- extra_ingredients must not contain duplicates.

Format:

{{
  "suggestions": [
    {{
      "title": "Dish Name",
      "ingredients_used": "onion, tomato",
      "extra_ingredients": "oil, salt",
      "steps": [
        "Detailed step 1",
        "Detailed step 2"
      ],
      "cook_time": "20 minutes",
      "difficulty": "Easy"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    ai_text = response.choices[0].message.content.strip()

    if ai_text.startswith("```json"):
        ai_text = ai_text.replace("```json", "").replace("```", "").strip()

    return json.loads(ai_text)