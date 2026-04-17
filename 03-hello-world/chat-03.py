from dotenv import load_dotenv
import google.generativeai as genai

import os
import re, json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



# Chain of Thought prompting :Model is encouraged to break down reasoning step by step before arriving to the answer. 
SYSTEM_PROMPT="""
  You are an helpful AI assistant who is specialized in resolving user query.
  For the given user input,analyze the input and break down the problem step by step.
  The steps are you get a user input, you analyze ,you think and you think again, and think for several times and then return the output with an explaination.
  Follow the steps in sequence that is "analyse" , "think" ,"output", "validate" and finally "result".

  Rules:
  1.Follow the strict JSON output as per schema.
  2.Always perform one step at a time and wait for the next input.
  3.Carefully analyze the user query.

  Example:
  Input:what is the value of 2+2?
  output:{{"step":"analyze"."content":"Alright the user is interset in maths query and he is asking a basic maths problem."}}
  output:{{"step":"think","content":"to perform this operetion i must go from left to right and add all the operands"}}
  output:{{"step":"output","content":"4"}}
  output:{{"step":"validate","content":"Seems like 4 is correct ans for 2+2"}}
  output:{{"step":"result","content":"2+2=4 and this is calculated by adding all numbers"}}



"""
model = genai.GenerativeModel("gemini-2.5-flash")


# messages = [

#     {"role": "model", "parts": [SYSTEM_PROMPT]},  

#     {"role":"user","parts":["What is 8*2+4 to the power of 3 to the power 4"]},
#     {"role":"user","parts":[json.dumps({
#   "step": "analyze",
#   "content": "The user is asking to evaluate a mathematical expression involving multiplication, addition, and nested exponentiation. The phrasing '4 to the power of 3 to the power 4' implies right-to-left associativity for the exponents, meaning it's 4^(3^4)."
# })]},
# {"role":"user","parts":[json.dumps({
#   "step": "think",
#   "content": "To evaluate '8*2+4 to the power of 3 to the power 4', I need to follow the order of operations (PEMDAS/BODMAS): exponents first, then multiplication, then addition. For nested exponents like 'a to the power of b to the power c', it's calculated as a^(b^c). \n\n1.  **Innermost exponent:** Calculate 3 to the power of 4 (3^4).\n2.  **Outer exponent:** Use the result from step 1 as the exponent for 4 (4^(result of 3^4)).\n3.  **Multiplication:** Calculate 8 multiplied by 2 (8*2).\n4.  **Addition:** Add the result from step 3 to the result from step 2."
# })]},
#  {"role":"user","parts":[json.dumps({
#   "step": "output",
#   "content": "16 + 4^81"
# })]},
# {"role":"user","parts":[json.dumps({
#   "step": "validate",
#   "content": "The expression was '8*2 + 4 to the power of 3 to the power 4'.\nFollowing order of operations:\n1.  Innermost exponent: 3 to the power of 4 (3^4) = 81.\n2.  Outer exponent: 4 to the power of 81 (4^81).\n3.  Multiplication: 8*2 = 16.\n4.  Addition: 16 + 4^81.\nThe output '16 + 4^81' correctly reflects these steps and represents the fully simplified form of the expression before calculating the very large number 4^81."
# })]},
# ]

messages=[
  {"role":"model","parts":[SYSTEM_PROMPT]}
]



last_step = None

while True:
  query=input("> ")
  # messages.append({"role":"user","parts":[query]})
  new_messages = [
    {"role": "model", "parts": [SYSTEM_PROMPT]},
    {"role": "user", "parts": [query]}
  ]
  
  while True:
    # Passing the json Data to the model
    response = model.generate_content(new_messages,generation_config={"response_mime_type": "application/json","temperature": 0.0})
    raw_output = response.text.strip()
    def extract_json(text):
      """Extract first valid JSON object from model text output."""
      match = re.search(r'\{.*?\}', text, flags=re.DOTALL)
      if not match:
          return None
      try:
          return json.loads(match.group(0))
      except json.JSONDecodeError:
          return None

    parsed_response = extract_json(raw_output)
    # parsed_response=json.loads(raw_output)
    # checking if object is coming or not 
    if isinstance(parsed_response, list):
          if len(parsed_response) > 0:
              parsed_response = parsed_response[0]
          else:
              print("⚠️ Empty list from model")
              break
    # messages.append({"role":"model","parts":[raw_output]})
    step = parsed_response.get("step")
    if step != last_step:
      new_messages.append({"role": "model", "parts": [raw_output]})
      last_step = step  # Update last_step
    if parsed_response.get("step")!="result":
      print("   🧠:", parsed_response.get("step"), "->", parsed_response.get("content"))
      continue

    print("🤖:", parsed_response.get("step"), "->", parsed_response.get("content"))
    break

# if response.text:
# print(response.text)
# else:
#     # Inspect raw structure
#     print("No text in response. Raw response:")
#     print(response)