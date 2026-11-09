# Standard Imports
import os

# Third Party Imports
from openai import OpenAI
from dotenv import load_dotenv

# Local Imports
from tools import TOOLS, tool_call_handler
from Utilities.utilities import log

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = []

messages.append({"role":"system","content":"You are a helpful assistant, and try answer every query in  details using bullet points."})

while True:
    input_text = input("\n🧑 You: ");
    if(input_text.lower() in ["exit", "quit", "bye"]):
        print("Exiting the chat. Goodbye!")
        break

    messages.append({
        "role" : "user",
        "content" : input_text
    })

    maxSteps = 5
    # Chained Tool Calling

    for step in range(maxSteps):
        response = client.chat.completions.create(
                model = os.getenv("MODEL"),
                messages = messages,
                tools = TOOLS,
            )
        
        msg = response.choices[0].message

        if not msg.tool_calls:
            break

        log(f"📝 Step {step+1}: Tool call detected. Model Requested {len(msg.tool_calls)} tool calls.")

        messages.append(msg)

        for tool_call in msg.tool_calls:

            res = tool_call_handler(tool_call)  # Call the tool and get the result

            log(f"  ↪️ Tool Call Result: {res}")

            messages.append({
                "role" : "tool",
                "tool_id" : tool_call.id,
                "content" : res
            })

    else:      # The else block runs only if the loop finished normally, without break
        fallback = "Maximum steps reached. Please try again with a simpler query."
        messages.append({
            "role" : "assistant",
            "content" : fallback
        })

        print("🤖 Assistant: " + fallback)
        continue

    messages.append({
        "role" : "assistant",
        "content" : msg.content
    })

    print("🤖 Assistant: " + msg.content)



















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