import json
from pyexpat.errors import messages

from dotenv import load_dotenv
from openai import OpenAI
import requests
import os
load_dotenv()

client=OpenAI()

def run_command(command:str):
    result=os.system(command)
    return result

def get_weather(city:str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_res = requests.get(geo_url).json()

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    # Step 2: Get weather
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_res = requests.get(weather_url).json()

    temp = weather_res["current_weather"]["temperature"]

    return f"The current temperature in {city} is {temp}°C"


available_tools={
    "get_weather":get_weather,
    "run_command":run_command
}

SYSTEM_PROMPT=f"""
you are an assistant designed to help users with various tasks.

You work on start,plan, action and observe loop.
For the given user and available tools, plan the step by step execution ,based on the planning ,
select the relevant tool from the avilabe tool 
and based on the tool selection you perform an action to call the tool.

wait for the observation and based on the observation from the tool , resolve the user query.

Rules:
-Follow the output json format
-Always perform one step at a time and wait for the next input 
-Carefully analyze the query

Output JSON format:
{{
    "step":"string",
    "content":"string",
    "function":"the function name for action step",
    "input":"the input for the function in action step",
}}

Available tools:
1. get_weather: This tool takes a city name as input and returns the current temperature in that city.
2. run_command: This tool takes a command as input and executes it and returns the output after executing it.

Example:
User query: "what is the current weather in new York?"
Output:{{"step":"plan","content":"From the available tools, I will select the most
 relevant one based on the user query and my analysis. Then I will call the tool with the 
 appropriate input and wait for the observation to resolve the user query."}}
Output:{{"step":"action","function":"get_weather","input":"new York"}}
Output:{{"step":"observe","output":"the current temperature in new York is 20°C"}}
Output:{{"step":"output","content":"the weather for newYork seems to be 20°C"}}

For output of run_command , always keep in mind that
- Always analyze tool output carefully
- If tool output contains "ERROR" or failure, do NOT assume success
- If command fails, correct it and try again
- Commands must be compatible with Windows OS
- The system is running on Windows
- Use Windows-compatible commands only

"""

messages=[
    {"role":"system","content":SYSTEM_PROMPT}
]

while True:
    query=input("> ")
    messages.append({"role":"user","content":query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({"role":"assistant","content":response.choices[0].message.content})
        parsed_response=json.loads(response.choices[0].message.content)
        if parsed_response.get("step")=="plan":
            print(f"🧠 {parsed_response.get('content')}")
            continue
        if parsed_response.get("step")=="action":
            tool_name=parsed_response.get("function")
            tool_input=parsed_response.get("input")

            print(f"🔧 Calling tool {tool_name} with input {tool_input}")
            
            # if the available tool found
            if available_tools.get(tool_name)!=False:
                output=available_tools[tool_name](tool_input)
                messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
                continue

        if(parsed_response.get("step")=="output"):
            print(f"✅ Final output: {parsed_response.get('content')}")
            break
print("Response from the model: ", response.choices[0].message.content)