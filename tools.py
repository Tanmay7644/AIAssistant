from datetime import datetime
import requests
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = "https://wttr.in/"+city+"?format=3"

    response = requests.get(url,timeout=10)

    return response.text

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
                }
            }
        }
    }


]

function_map = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather
}