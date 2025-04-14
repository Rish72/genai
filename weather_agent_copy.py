import dotenv
from openai import OpenAI
import os
import json
import requests

gpt_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=gpt_key
)

def get_weather(city: str) :
    url = f"https://wttr/{city}?format=%C+%t"
    res = requests.get(url)
    
    if res.status_code(200):
        return res.text
    return "unable to fetch the record"

available_tools =  {
    get_weather : {
        "fn" : "get_weather",
        "desc" : "A tool function that takes city and return its temperature and weather"
    },
}

system_prompt = """
    You are an helpfull ai assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning, select the relevant tool from the available tool. and baed on the tool selection you perform an action to call the tool
    Wait for the obervation and based on the observation from the tool call resolve the user query 
    
    Rules:
        1. Follow the strict JSON output as per Output schema.
        2. Always perform one step at a time and wait for next input
        3. Carefully analyse the user query
        
    Available Tools : 
        - get_weather : Takes a city as input and return the weather of the provided city
    
    
    output json format :
     {{
         "step" : "string",
          "content" : "string",
          "function" : "the name of the function if the step is action ",
          "input" : "input parameter of the function"
     }}
    
    Example :
        User query : What is the weather of New Delhi?
        Output : {{"step" : "plan" , "content" : "The user is interested in the weather data of New delhi"}}
        Output : {{"step" : "plan" , "content" : "From the available tools I should call get_weather"}}
        Output : {{"step" : "action" , "function" : "get_weather", "input" : "new delhi"}}
        Output : {{"step" : "observe" , "output" : "12 Degree celcius"}}
        Output : {{"step" : "output" , "content" : "The weather of new delhi seems to be 12 Degree celcius"}}
"""

messages = [
    {"role" : "system" , "content" : system_prompt}
]

user_query = input("> ")
messages.append({"role" : "user" , "content" : user_query})


while True : 
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type" : "json_object"},
    )
    
    parsed_res = json.loads(response.choices[0].message.content)
    
    messages.append({"role" : "system" , "content" : json.dumps(parsed_res)})
    
    if parsed_res.get("step") == "plan" : 
        print(f"🧠 : {parsed_res.get("content")}")
        continue
    
    if parsed_res.get("step") == "action" :
        tool_name = parsed_res.get("function")
        tool_input = parsed_res.get("input")
        
        if available_tools.get(tool_name, False) != False : 
            output = available_tools[tool_name].get("fn")(tool_input)
            messages.append({"role" : "assistant" , "content" : json.dumps({"step" : "observe" , "content" : output})})
            
    if parsed_res.get("step") == "output" :
        print(f"🤖 : {parsed_res.get("content")}")
        break
        