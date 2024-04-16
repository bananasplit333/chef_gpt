import json
import requests
from .chat_completion import groq_completion_request
from bs4 import BeautifulSoup



#extract contents from url 
def extract_text_from_url(url):
    try:
        # Headers for bs
        headers = {'User-Agent': 'Mozilla/5.0'}

        # Send a GET request to the URL
        response = requests.get(url, headers=headers)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the JSON-LD script
        script_tag = soup.find('script', type='application/ld+json')

        if script_tag:
            json_data = script_tag.string
            data = json.loads(json_data)
            return data
        else:
            print('JSON-LD data not found')
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the URL: {e}")
        return None


#extract ingredients from json object 
def extract_recipe_ingredients(json_data):
    # Set system message 
    messages = [
        {
            "role": "system",
            "content": """You are a helpful JSON extractor bot that will be given some JSON data.
                            Specifically, you will be responsible for looking at JSON-LD data and extracting the values for the ingredients list AND cooking instructions from the table.  
                            Please extract the text and return it in this format:
                            
                            {
                            'ingredients': ['chicken breast', '2 eggs', '3 lb potatoes']
                            },
                            
                            Please make sure to only include the relevant text. Try to filter out any newspace or @type, or "howtostep"
                            """

        },
        {
            "role": "user",
            "content": json.dumps(json_data)
        }
    ]
    #call chat completion 
    try: 
        chat_completion = groq_completion_request(messages=messages, tool_choice="none")
        return chat_completion.choices[0].message.content
    #chat completion not completed 
    except Exception as e: 
        print("Unable to extract ingredients")
        print(f"Exception: {e}")
        return e

#extract instructions from the json object 
def extract_instructions(json_data):
    # Set system message 
    messages = [
        {
            "role": "system",
            "content": """You are a helpful JSON extractor bot that will be given some JSON data.
                            Specifically, you will be responsible for looking at JSON-LD data and extracting the values for the ingredients list AND cooking instructions from the table.  
                            Please extract the text and return it in this format:
                            
                            {
                            'cooking_instructions': ['finely dice some onions', 'salt some water, put it to a boil in a pot.', 'add some peppers', ...]
                            },
                            
                            Please make sure to only include the relevant text. Try to filter out any newspace or @type, or "howtostep"
                            """

        },
        {
            "role": "user",
            "content": json.dumps(json_data)
        }
    ]
    #call chat completion 
    try: 
        chat_completion = groq_completion_request(messages=messages, tool_choice="none")
        return chat_completion.choices[0].message.content
    #chat completion not completed 
    except Exception as e: 
        print("Unable to extract cooking instructions")
        print(f"Exception: {e}")
        return e
