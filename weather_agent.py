import dotenv
from openai import OpenAI
import os
import json
import requests

gpt_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=gpt_key
)

def get_weather(city : str) : 
    url = f"https://wttr.in/{city}?format=%C+%t"
    res = requests.get(url)
    if res.status_code(200) : 
        return {"Weather in {city} is {res.text}"}
    return "31 degree"

available_tools = {
    get_weather : {
        "fn" : get_weather,
        "desc" : "Takes city as input and find the current weather of the city"
    }
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
    {"role" : "system", "content" : system_prompt}
]
query = input("> ");

messages.append({"role" : "user" , "content" : query})


while True :
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= messages,
        response_format={"type" : "json_object"},
    )
    
    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role" : "assistant" , "content" : json.dumps(parsed_response)})
    
    if parsed_response.get("step") == "plan" : 
        print(f"🧠 : {parsed_response.get("content")}")
        continue
    
    
    # Agr step action h to function ko call krna chahiye
    if parsed_response.get("step") == "action" : 
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")
        if available_tools.get(tool_name , False) != False :
            output = available_tools[tool_name].get("fn")(tool_input)
            messages.append({"role" : "assistant", "content" : json.dumps({"step":"observe", "output": output})})
    
    if parsed_response.get("step") == "output" : 
        print(f"🤖 : {parsed_response.get("content")}")
        break;
        