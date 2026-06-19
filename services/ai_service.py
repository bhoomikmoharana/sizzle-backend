import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_recipes(ingredients: list[str]):
    ingredients_text = ", ".join(ingredients)

    prompt = f"""
You are an expert Indian home chef for a cooking app called Sizzle AI.

User ingredients:
{ingredients_text}

Suggest exactly 3 dishes.

Rules:
- Return ONLY valid JSON.
- No markdown.
- No explanation outside JSON.
- Recipes should be beginner friendly and realistic for home/hostel cooking.
- Each recipe must have 6 to 8 detailed cooking steps.
- Each step should be 1 to 2 sentences long.
- Mention heat level where useful: low, medium, or high.
- Mention approximate cooking time where useful.
- Mention visual cues like "until onions turn translucent", "until tomatoes become mushy", "until oil separates", "until golden brown".
- Use simple Indian cooking language.
- Do not make the recipes too fancy.
- ingredients_used must not contain duplicates.
- extra_ingredients must not contain duplicates.

Bad step:
"Fry onions."

Good step:
"Heat 2 tablespoons oil in a pan or kadai over medium heat. Add chopped onions and sauté for 3 to 4 minutes until they turn soft and light golden."

Format:

{{
  "suggestions": [
    {{
      "title": "Dish Name",
      "ingredients_used": "onion, tomato, potato",
      "extra_ingredients": "oil, salt, turmeric powder, red chilli powder",
      "steps": [
        "Detailed step 1.",
        "Detailed step 2.",
        "Detailed step 3.",
        "Detailed step 4.",
        "Detailed step 5.",
        "Detailed step 6."
      ],
      "cook_time": "25 minutes",
      "difficulty": "Easy"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.7,
        max_tokens=3000,
    )

    ai_text = response.choices[0].message.content.strip()

    if ai_text.startswith("```json"):
        ai_text = ai_text.replace("```json", "").replace("```", "").strip()

    return json.loads(ai_text)