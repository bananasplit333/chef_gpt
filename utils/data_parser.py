import json
import re
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
            print("paring parameters...")
            #extract necessary data
            ingredients = extract_value(data, 'recipeIngredient')
            instructions = extract_value(data, 'recipeInstructions')
            name = extract_value(data, 'headline')
            prepTime = extract_value(data, 'prepTime')
            cookTime = extract_value(data, 'cookTime')
            recipe_yield = extract_value(data, 'recipeYield')
            print(f'yields {recipe_yield}')
            print(f'TITLE : {name}')
            print(prepTime)
            #clean instructions 
            filtered_instructions = clean_instructions(instructions)
            filtered_cookTime = clean_timing(str(cookTime))
            filtered_prepTime = clean_timing(str(prepTime))
            
            print(f'prep_time {filtered_prepTime}')
            

            data_obj = {
                'ingredients': ingredients if ingredients else None,
                'cooking_instructions': filtered_instructions if filtered_instructions else None,
                'name': name if name else None,
                'prep_time': filtered_prepTime if filtered_prepTime else None,
                'cook_time': filtered_cookTime if filtered_cookTime else None,
                'recipe_yield': recipe_yield if recipe_yield else None
            }

            return data_obj
        else:
            print('JSON-LD data not found')
            return ValueError
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the URL: {e}")
        return None

def extract_first_number(string):
    match = re.search(r'\d+', string)
    if match:
        return int(match.group())
    else:
        return None

def extract_ingredients(obj):
    try:
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'recipeIngredient':
                    yield value
                else:
                    yield from extract_ingredients(value)
        elif isinstance(obj, list):
            for item in obj:
                yield from extract_ingredients(item)
    except Exception as e: 
        print('extract_ingredients failed')
        return e 
    

#extract values from json ld data. 
def extract_value(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for value in obj.values():
            result = extract_value(value, key)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = extract_value(item, key)
            if result is not None:
                return result
    return None

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

#clean time format
def clean_timing(str):
    # Pattern to match "P0DT0H10M0S" format
    pattern = r"P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
    # Extract hours and minutes using regular expression
    match = re.match(pattern, str)
    if match:
        years = int(match.group(1)) if match.group(1) else 0
        months = int(match.group(2)) if match.group(2) else 0
        days = int(match.group(3)) if match.group(3) else 0
        hours = int(match.group(4)) if match.group(4) else 0
        minutes = int(match.group(5)) if match.group(5) else 0
        seconds = int(match.group(6)) if match.group(6) else 0
    else:
        hours = 0
        minutes = 0
    if hours > 0: 
        output = f"{hours}h{minutes}min"
    else:
        output = f"{minutes}min"
    return output 