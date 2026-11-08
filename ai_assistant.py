import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS, function_map

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

messages.append({"role":"system","content":"You are a funny assistant, and try answer every query under 25 words."})

while True:
    input_text = input("\nYou: ");
    if(input_text.lower() in ["exit", "quit", "bye"]):
        print("Exiting the chat. Goodbye!")
        break

    messages.append({
        "role" : "user",
        "content" : input_text
    })

    # Chained Tool Calling

    while True:
        response = client.chat.completions.create(
                model = os.getenv("MODEL"),
                messages = messages,
                tools = TOOLS,
            )
        
        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        messages.append(msg)

        for tool_call in msg.tool_calls:
            # handling exceptions for tool calls
            function_name = tool_call.function.name
            function_args = {}

            try:
                function_args = json.loads(tool_call.function.arguments or "{}")   # convert string to dict 
                fn = function_map[function_name]
                res = fn(**function_args)  # unpack the dict as keyword arguments
            except Exception as e:
                res = f"Error calling tool {function_name}: {str(e)}"

            messages.append({
                "role" : "tool",
                "tool_id" : tool_call.id,
                "content" : res
            })


    messages.append({
        "role" : "assistant",
        "content" : msg.content
    })

    print("Assistant: " + msg.content)



















# Without Tool Calling

# while True:
#     input_text = input("\nYOU: ")


#     if input_text.lower() in ["exit", "quit", "bye"]:
#         print("Exiting the chat. Goodbye!")
#         break

#     messages.append({"role":"user","content":input_text})

#     response = client.chat.completions.create(
#         model = os.getenv("MODEL"),
#         messages=messages
#     )

#     messages.append({"role":"assistant","content":response.choices[0].message.content})
#     print("Assistant: " + response.choices[0].message.content)