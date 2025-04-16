from fastapi import FastAPI
from ollama import Client
from fastapi import Body

app = FastAPI()
client = Client(
    host = 'http://localhost:11434'
)

client.pull("gemma3:4b")

@app.get('/')
def get() : 
    return {"message" : "WElcome to your fastapi get page"}

@app.post('/chat')
def chat() : 
    response = client.chat(
        model="gemma3:4b", 
        messages=[
            {"role" : "user","content" : "What is the name of jupiter moons" }
        ]    
    )
    # print(respone.)
    return response['message']['content']  

# def chat(message: str = Body(..., description="Chat Message")):
#     response = client.chat(model="gemma3:1b", messages=[
#         { "role": "user", "content": message }
#     ])

#     return response['message']['content']