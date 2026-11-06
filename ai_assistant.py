from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

while True:
    input_text = input("\nYOU: ")

    if input_text.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat. Goodbye!")
        break

    response = client.chat.completions.create(
        model = os.getenv("MODEL"),
        messages=[
            {"role": "system", 
            "content": input_text},
        ]
    )

    print("Assistant: " + response.choices[0].message.content)
