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

messages.append({"role":"system","content":"You are a helpful assistant."})

while True:
    input_text = input("\nYou: ");
    if(input_text.lower() in ["exit", "quit", "bye"]):
        print("Exiting the chat. Goodbye!")
        break

    messages.append({
        "role" : "user",
        "content" : input_text
    })

    response = client.chat.completions.create(
        model = os.getenv("MODEL"),
        messages = messages,
        tools = TOOLS,
    )

    msg = response.choices[0].message

    if msg.tool_calls:

        messages.append(msg)

        for tool_call in msg.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments or "{}")   # convert string to dict 

            fn = function_map[function_name]

            res = fn(**function_args)  # unpack the dict as keyword arguments

            messages.append({
                "role" : "tool",
                "tool_id" : tool_call.id,
                "content" : res
            })


        # 2nd call to LLM
        response = client.chat.completions.create(
            model = os.getenv("model"),
            messages = messages
        )

        msg = response.choices[0].message

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
