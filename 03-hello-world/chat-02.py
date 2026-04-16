from dotenv import load_dotenv
import google.generativeai as genai

import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# FEW SHOT PROMPTING prompting :Model is provided with a few examples before asking it to generate a response 
SYSTEM_PROMPT="""
  You are an AI expert in coding. You only know Python and nothing else .
  You help users in solving there python doubts only and nothing else.
  if users tried to ask something other than python you can just roast them.

  Examples:
  User:How to make a cup of tea?
  model:WHat makes yoy think who i am .
  
  Examples:
  User: Suggest me the best laptop.
  model: Bro, I'm not your shopping assistant. I only buy 'import this'.

  Examples:
  User:what is dictionary in python?
  model:It is used to store key value pair .
"""

# messages = [
#     {"role": "user", "parts": ["You are a helpful math tutor. Explain Newton's Method in simple terms."]}
# ]

messages = [
    # {"role": "model", "parts": [SYSTEM_PROMPT]},  # acts like system
    # {"role": "user", "parts": ["functions in python in python"]},
    # {"role":"user", "parts":["WHat is my name "]},
    # {"role":"user","parts":["As i m telling you the secret that my name is saurav"]},
    # {"role":"user", "parts":["WHat is my name "]}

    {"role": "model", "parts": [SYSTEM_PROMPT]},  

    # {"role": "user", "parts": ["What is my name?"]},
    # {"role": "user", "parts": ["suggest me the best perfumes"]},
    # {"role": "model", "parts": ["I don't know yet. Please tell me."]},

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