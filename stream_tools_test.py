from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS

load_dotenv()

client = OpenAI(
    base_url = os.getenv("BASE_URL"),
    api_key = os.getenv("API_KEY")
)

stream = client.chat.completions.create(
    model = os.getenv("MODEL"),
    messages = [
        {"role":"system","content":"You are a helpful assistant, and try answer every query in  details using bullet points."},
        {"role":"user","content":"What is the weather of pune and weather of banglore?"}
    ],
    tools = TOOLS,
    stream = True 
)

for chunk in stream:
    if not chunk.choices:
        continue

    msg = chunk.choices[0].delta

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            
            print(tool_call, end="", flush=True)