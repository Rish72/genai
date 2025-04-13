import os
import json
from dotenv import load_dotenv

from openai import OpenAI
from google import genai
from google.genai import types

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

genai_client = genai.Client(api_key=gemini_key)
gpt_client = OpenAI(
    api_key = openai_key
)


def asking_gpt(prompt) : 
    response = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages= [
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : prompt}
        ]
    )
    
    return response.choices[0].message.content
    
def asking_gemini(prompt) : 
    response = genai_client.models.generate_content(
        model="gemini-2.5-pro-exp-03-25",
        contents= prompt,
        config= types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )
    return response.text

def selection_ai(opt_1, opt_2) : 
    res = gpt_client.chat.completions.create(
        model='gpt-4o',
        messages= [
            {"role" : "system", "content": selection_prompt},
            {"role" : "user", "content": f"Here are two options:\nOption 1: {opt_1}\nOption 2: {opt_2}\nPlease analyze and tell which one is better and why."}

        ]
    )
    return res.choices[0].message.content

system_prompt = """
    You are an AI assistant answer precisely every question and concise answer with posing as a human.
    
    Rules : 
        1. Answer concise
        2. Answer the asking question in a way humans answer
"""
selection_prompt = "You are an expert ai assistant whose job to find the most appropriate human like answer between two responses. first give the response of the selected option then from the next line explain why was it better?"

query = input("> ")

gemini_res = asking_gemini(query)
gpt_res = asking_gpt(query)

print("gpt response : ", selection_ai(gemini_res, gpt_res))



# TechSupport