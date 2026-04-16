from dotenv import load_dotenv
import google.generativeai as genai

import os

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# FEW SHOT PROMPTING prompting :Model is provided with a few examples before asking it to generate a response 
SYSTEM_PROMPT="""
  Ypu are an AI persona of Hitesh
"""

messages = [

    {"role": "model", "parts": [SYSTEM_PROMPT]},  


    {"role": "user", "parts": ["My name is Saurav."]},
    # {"role": "model", "parts": ["Got it! Your name is Saurav."]},

# {"role": "user", "parts": ["What is my name?"]}

    # {"role": "model", "parts": ["What makes you think who I am."]},
    # {"role": "user", "parts": ["How to score 90% in exams"]}  # actual user question
]

response = model.generate_content(messages)

if response.text:
    print(response.text)
else:
    # Inspect raw structure
    print("No text in response. Raw response:")
    print(response)