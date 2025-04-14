import dotenv
from openai import OpenAI
import os


gpt_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=gpt_key)

system_prompt ="""
    
"""