import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


stream = client.chat.completions.create(
    model = os.getenv("MODEL"),
    messages = [
        {"role":"system","content":"You are a helpful assistant, and try answer every query in  details using bullet points."},
        {"role":"user","content":"Explain the concept of recursion in programming."}
    ],
    stream = True
)

for chunk in stream:
    if not chunk.choices:
        continue

    piece = chunk.choices[0].delta.content
    if piece:
        print(piece, end="", flush=True)
