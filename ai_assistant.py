# Standard Imports
import os
from types import SimpleNamespace

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

messages.append({"role":"system","content":"You are a helpful assistant, and try answer every query in details using bullet points."})

def stream_chat(messages):
    """
    This function streams the chat response from the model and collects any tool calls made by the model.
    """

    stream = client.chat.completions.create(
        model = os.getenv("MODEL"),
        messages = messages,
        tools = TOOLS,
        stream = True
    )  

    full_response = ""
    calls = {}
    label_printed = False

    try:
        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta


            # 1. content streaming
            if delta.content:
                if not label_printed:
                    print("🤖 Assistant: ", end="", flush=True)
                    label_printed = True

                print(delta.content, end="", flush=True)

                full_response += delta.content


            # 2. tool call streaming
            if delta.tool_calls:
                for tc in delta.tool_calls:
                        print(f"Tool Call Detected: {tc.function.name} with arguments: {tc.function.arguments}")
                
                        if tc.index not in calls:
                            calls[tc.index] = SimpleNamespace(id = None, function = SimpleNamespace(name = "", arguments = ""))
                
                        obj = calls[tc.index]
                
                        if tc.id:
                            obj.id = tc.id
                        if tc.function.name:
                            obj.function.name += tc.function.name
                        if tc.function.arguments:
                            obj.function.arguments += tc.function.arguments
    except KeyboardInterrupt as e:
        print("\nStreaming interrupted by user.")
        calls = {} # Reset calls if interrupted

    if label_printed:
        print()  # Move to the next line after streaming is done

    calls_list = []
    for key in sorted(calls):
        calls_list.append(calls[key])

    return full_response, calls_list


def build_tool_call_payload(tool_calls):
    """
    It converts collected tool calls (string format) into a structured payload that can be sent back to the model for further processing.
    """

    payload = []

    for too_call in tool_calls:
        payload.append({
            "id": too_call.id,
            "type": "function",
            "function": {
                "name": too_call.function.name,
                "arguments": too_call.function.arguments
            }
        })

    return payload

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

        full_response, tool_calls = stream_chat(messages)

        if not tool_calls:
            break

        log(f"📝 Step {step+1}: Tool call detected. Model Requested {len(tool_calls)} tool calls.")

        messages.append({
            "role" : "assistant",
            "content" : full_response,
            "tool_call" : build_tool_call_payload(tool_calls)  # we need all payload

                # tool_call => {
                #     id: tool_call.id,
                #     function: {
                #         name: tool_call.name,
                #         arguments: tool_call.arguments
                #     }
                # }
        })

        for tool_call in tool_calls:

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






