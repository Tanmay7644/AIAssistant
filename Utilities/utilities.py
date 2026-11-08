import os

START_SEQUENCE = "\033[90m"   # grey text
END_SEQUENCE = "\033[0m"      # reset

def log(text):
    if(os.getenv("DEBUG") == "True"):
        print(f"    {START_SEQUENCE}{text}{END_SEQUENCE}")