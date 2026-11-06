from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

messages.append({"role":"system","content":"You are a helpful assistant."})

while True:
    input_text = input("\nYOU: ")


    if input_text.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat. Goodbye!")
        break

    messages.append({"role":"user","content":input_text})

    response = client.chat.completions.create(
        model = os.getenv("MODEL"),
        messages=messages
    )

    messages.append({"role":"assistant","content":response.choices[0].message.content})
    print("Assistant: " + response.choices[0].message.content)
