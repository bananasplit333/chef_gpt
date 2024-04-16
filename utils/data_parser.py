import json
import requests
from .chat_completion import groq_completion_request
from bs4 import BeautifulSoup

#extract contents from url 
def extract_text_from_url(url):
    print(url)
    try:
        # Headers for bs
        headers = {'User-Agent': 'Mozilla/5.0'}

        # Send a GET request to the URL
        response = requests.get(url, headers=headers)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the JSON-LD script
        script_tag = soup.find('script', type='application/ld+json')

        #JSON-LD FOUND 
        if script_tag:
            json_data = script_tag.string
            data = json.loads(json_data)
            
            #get the ingredients from filtered data 
            ingredients = extract_ingredients(data)
            print("INGREDIENTS")
            print(ingredients)
            filtered_ingredients = clean_ingredients(ingredients)
            #get the rough instructions from filtered data 
            instructions = extract_instructions(data)
            #further filtering 
            filtered_instructions = clean_instructions(instructions)
            print(filtered_instructions)

            #compile into object to return 
            data_obj = {'ingredients':list(ingredients), 'cooking_instructions':filtered_instructions}
            print("DATA OBJ:")
            print(data_obj)
            return data_obj
        else:
            print('JSON-LD data not found')
            return ValueError
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the URL: {e}")
        return None

def extract_ingredients(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'recipeIngredient':
                yield value
            else:
                yield from extract_ingredients(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from extract_ingredients(item)

def extract_instructions(obj):
    instructions = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'recipeInstructions':
                instructions.append(value)
            else:
                instructions.extend(extract_instructions(value))
    elif isinstance(obj, list):
        for item in obj:
            instructions.extend(extract_instructions(item))
    return instructions

def clean_ingredients(extracted_ingredients):
    messages = [
         {
            "role": "system",
            "content": """You are a helpful JSON extractor bot that will be given some JSON data.
                            Specifically, you will be responsible for extracting the values for the cooking instructions from the table.  
                            Please extract the text and return it in this format:
                            
                            **
                            {
                            "'ingredients': ['onions, sliced', '2 lb potatoes', ...]
                            },
                            **

                            Please make sure to only include the relevant text. Try to filter out any newspace or @type, or "howtostep"
                            """

        },
        {
            "role": "user",
            "content": str(extract_ingredients)
        }
    ]
#clean instructions from the json object 
def clean_instructions(extracted_instructions):
    # Set system message 
    messages = [
        {
            "role": "system",
            "content": """You are a helpful JSON extractor bot that will be given some JSON data.
                            Specifically, you will be responsible for extracting the values for the cooking instructions from the table.  
                            Please extract the text and return it in this format:
                            
                            **
                            {
                            "cooking_instructions": [instructions...]
                            },
                            **

                            Please make sure to only include the relevant text. Try to filter out any newspace or @type, or "howtostep"
                            """

        },
        {
            "role": "user",
            "content": str(extracted_instructions)
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

