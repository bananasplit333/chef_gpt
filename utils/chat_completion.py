import os 
from groq import Groq 
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt

#load API 
load_dotenv()
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
GROQ_MODEL = "mixtral-8x7b-32768"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def groq_completion_request(messages, tools=None, tool_choice=None, model=GROQ_MODEL):
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            response_format={"type": "json_object"},
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def groq_completion_request_basic(messages, tools=None, tool_choice=None, model=GROQ_MODEL):
    try:
        response = groq_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e