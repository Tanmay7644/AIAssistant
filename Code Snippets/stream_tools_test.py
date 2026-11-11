from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS
from types import SimpleNamespace

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


calls = {}

for chunk in stream:
    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta

    for tc in delta.tool_calls:
        print(f"Tool Call Detected: {tc.name} with arguments: {tc.arguments}")


        if not calls[tc.index]:
            calls[tc.index] = SimpleNamespace(id = None, function = SimpleNamespace(name = "", arguments = ""))

        obj = calls[tc.index]

        if tc.id:
            obj.id = tc.id
        if tc.name:
            obj.function.name += tc.name
        if tc.arguments:
            obj.function.arguments += tc.arguments


calls_list = []
for key in sorted(calls):
    calls_list.append(calls[key])