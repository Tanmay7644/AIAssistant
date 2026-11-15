#standard Imports
import json

#Third-Party Imports
from datetime import datetime
import requests

#Local Imports
from Utilities.utilities import log
from rag import search

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = "https://wttr.in/"+city+"?format=3"
    response = requests.get(url,timeout=10)
    response.raise_for_status()
    return response.text

def get_my_city():
    return "Jamkhed"

def search_knowledge_base(query):
    results = search(query,2)
    log(f"Knowledge Base Search: {query}")
    for r in results:
        log(f"{r['score']:.2f} - {r['source']} - #{r['chunk_id']}")


    blocks = []

    for r in results:
        score = r["score"]
        source = r["source"]
        chunk_id = r["chunk_id"]
        text = r["text"]

        header = f"[{source} #{score}]"
        block = f"{header}\n{text}"

        blocks.append(block)

    return "\n\n".join(blocks)
    



TOOLS = [
    {
        "type" : "function",
        "function": {
            "name" : "get_current_time",
            "description" : "Get the current date and time in the format YYYY-MM-DD HH:MM:SS",
            "parameters" : {
                "type" : "object",
                "properties" : {},
            }
        }
    },
    {
        "type" : "function",
        "function": {
            "name" : "get_city_weather",
            "description" : "Get the current weather for a given city",
            "parameters" : {
                "type" : "object",
                "properties" :{
                    "city" : {
                        "type" : "string",
                        "description" : "The name of the city to get the weather for"
                    }
                },
                "required" : ["city"]
            }
        }
    },
    {
        "type": "function",
        "function" :{
            "name" : "get_my_city",
            "description" : "Get the city where the user is currently located, or the city where the user is currently living",
            "parameters" : {
                "type" : "object",
                "properties" : {},
            }
        }
    },

    {
        "type" : "function",
        "function" : {
            "name" : "search_knowledge_base",
            "description" : "Searches the Zorvex Technologies company knowledge base: leave, medical, HR, hiring, tech, incident "
                            "reports and travel expense policies. Use it for any question about company policies or documents. "
                            "Returns the most relevant passages with their source.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "query" : {
                        "type" : "string",
                        "description" : "The user's question, rewritten as a short, self-contained search query."
                    }
                },
                "required" : ["query"]
            }
        }
    }

]

function_map = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_my_city": get_my_city,
    "search_knowledge_base" : search_knowledge_base
}


def tool_call_handler(tool_call):
    function_name = tool_call.function.name
    function_args = {}

    log(f"📝 Tool Call: {function_name} with arguments: {tool_call.function.arguments}")

    try:
        function_args = json.loads(tool_call.function.arguments or "{}")   # convert string to dict 
        fn = function_map[function_name]
        res = fn(**function_args)  # unpack the dict as keyword arguments
    except Exception as e:
        res = f"Error calling tool {function_name}: {str(e)}"

    return res