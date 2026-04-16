from dotenv import load_dotenv
import google.generativeai as genai

import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# ONE SHORT PROMPTING or ZERO short prompting :Model is given a direct question or task
SYSTEM_PROMPT="""
  You are an AI expert in coding. You only know Python and nothing else .
  You help users in solving there python doubts only and nothing else.
  if users tried to ask something other than python you can just roast them.
"""

# messages = [-
#     {"role": "user", "parts": ["You are a helpful math tutor. Explain Newton's Method in simple terms."]}
# ]

messages = [
    {"role": "model", "parts": [SYSTEM_PROMPT]},  # acts like system
    {"role": "user", "parts": ["How to make a tea"]}  # actual user question
]

response = model.generate_content(messages)

if response.text:
    print(response.text)
else:
    # Inspect raw structure
    print("No text in response. Raw response:")
    print(response)