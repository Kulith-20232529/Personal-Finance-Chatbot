import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')

def extract_expense(text):
    prompt = f"""
    Extract expense details from this sentence:
    "{text}"

    Return ONLY JSON. No explanation.

    Format:
    {{
      "amount": number,
      "category": "string",
      "date": "YYYY-MM-DD"
    }}
    """

    response = model.generate_content(prompt)

    content = response.text
    print("GEMINI RAW:", content)

    # ✅ Extract JSON safely
    match = re.search(r'\{.*\}', content, re.DOTALL)

    if not match:
        raise ValueError("No JSON found")

    return json.loads(match.group())