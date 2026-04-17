from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

text="Saurav Chases Rimpu"

result = genai.embed_content(
        model="gemini-embedding-001",
        content=text
      )

print(len(result["embedding"]))