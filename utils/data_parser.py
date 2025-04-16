import json
import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .chat_completion import groq_completion_request, groq_completion_request_basic
from bs4 import BeautifulSoup
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


RECIPE_KEYWORDS = [
    "ingredient", "preheat", "mix", "bake", "heat", "whisk", "cook", "stir", "oven", "boil", "simmer",
    "chop", "slice", "dice", "grate", "blend", "pour", "add", "season", "garnish", "serve", "chill",
    "marinate", "fry", "roast", "grill", "steam", "sauté", "caramelize", "reduce", "knead", "fold",    
    "cup", "tsp", "tbsp", "teaspoon", "tablespoon", "min", "hour", "serve", "degrees", "serves", "yield", "cooking time",
    "prep time", "cook time", "recipe", "instructions", "method", "directions", "how to", "step", "procedure",
]

# Set up Chrome options to mimic a real browser
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run without GUI for efficiency
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
options.add_argument('--accept-language=en-US,en;q=0.9')
options.add_argument('--disable-blink-features=AutomationControlled')  # Avoid bot detection

#extract contents from url 
def extract_text_from_url(url):
    print(url)

    ## Set up Chrome options to mimic real human behavior
    # Initialize driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Load the page
        driver.get(url)
        time.sleep(5)  # wait for cloudflare checks / website loading

        # Get the rendered page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        text = soup.get_text()
        text_chunks = split_into_chunks(text, chunk_size=100)
        
        # extracct json LD data 
        script_tag = soup.find('script', type='application/ld+json')
        web_strings = script_tag.string 
        data = json.loads(web_strings)
        image_url = extract_value(data, 'thumbnailUrl')
        name = extract_value(data, 'headline')

        if (text_chunks):
            filtered_chunk = get_recipe_chunks(text_chunks)
            print('filtered chunk len:', len(filtered_chunk))

            #get recipe info from chunks
            recipe_info = extract_recipe("".join(filtered_chunk))
            json_data = json.loads(recipe_info)
            #extract necessary data
            title = json_data.get('title', None)
            recipeYield = json_data.get('yield', None)
            ingredients = json_data.get('ingredients', None)    
            washed_vegetables = wash_vegetables(ingredients)
            print('vegetables have been washed, ', washed_vegetables)
            instructions = json_data.get('cooking_instructions', None)
            prepTime = json_data.get('prep_time', None)
            cookTime = json_data.get('cook_time', None)
            totalTime = json_data.get('total_time', None)
            name = json_data.get('name', None)
            data_obj = {
                'img_url': image_url if image_url else None,
                'ingredients': washed_vegetables if washed_vegetables else None,
                'cooking_instructions': instructions if instructions else None,
                'name': name if name else title if title else None,
                'prep_time': prepTime if prepTime else None,
                'cook_time': cookTime if cookTime else None,
                'recipe_yield': recipeYield if recipeYield else None,
                'total_time': totalTime if totalTime else None,
            }

            print('data obj', data_obj)
            return data_obj
        else:
            print('JSON-LD data not found')
            return ValueError
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the URL: {e}")
        return None
    finally:
        driver.quit()

def wash_vegetables(ingredients): 
    quantity_pattern = re.compile(r'\d+\s\d+/\d+|\d+/\d+|\d+|[¼-¾⅐-⅟]')
    for item in ingredients: 
        temp = item.get('quantity', '')
        matches = quantity_pattern.findall(temp)
        item['quantity'] = ' '.join(matches) if matches else ''
    
    return ingredients


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

#split into chunks 
def split_into_chunks(text, chunk_size): 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(text)
    return texts

def extract_relevant_content(text): 
    #set system message
    messages = [
        {
            "role": "system",
            "content": """You are a helpful JSON extractor bot that will be given arrays of text.
                            Specifically, you will be responsible for extracting the values for the cooking instructions from the table.  
                            
                            Please go through the text and return the number that has the most relevance to the cooking instructions.
                            """
        }
    ]
    #chat completion
    try:
        for (i, text_chunk) in enumerate(text):
            messages.append(
                {
                    "role": "user",
                    "content": text_chunk
                }
            )
        chat_completion = groq_completion_request(messages=messages, tool_choice="none")
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("Unable to extract cooking instructions")

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
                            Specifically, you will be responsible for cleaning up the values of a given obj:
                            Go through the object and for any measurements that have fractions, encapsulate them in double quotes ""
                            An example is given below

                            **
                            {
                            "'ingredients': ['"1/4" cup onions, sliced', '2 "1/2" lb potatoes', ...]
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
def extract_recipe(extracted_instructions):
    # Set system message 
    messages = [
        {
            "role": "system",
            "content": """You are a helpful ingredient extractor bot that will be given some data.
                            Specifically, you will be responsible for extracting the values for the cooking instructions from the table.
                            Please extract the text and return it in a JSON format. 
                            For each ingredient, make sure to separate the ingredient name, quantity and unit from each other.
                            For quantity, make sure to include only numbers and fractions. Do not include any text.
                            For example, "2 cups soy sauce" should be separated into: 
                            {
                                "ingredient": "soy sauce",
                                "quantity": "2",
                                "unit": "cups"
                            }

                            
                            **
                            {
                            "title": "...",
                            "yield": "... servings",
                            "prep_time": "... min",
                            "cook_time": "... min",
                            "total_time": "... min",
                            "cooking_instructions": [
                                1. instructions
                                2. instructions
                                3. instructions...]
                            "ingredients": [
                                {"ingredient": "...", "quantity": "...", "unit": "cups, tbsp, tsp......"},
                                {"ingredient": "...", "quantity": "...", "unit": "..."},
                                {"ingredient":, "quantity":, "unit": }...]
                            },
                            **

                            Please make sure to only include the relevant text. Try to filter out any newspace or @type, or "howtostep". Return as a json object.
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


# Function to check if a chunk contains recipe-related keywords
def is_recipe_chunk(chunk, keywords = RECIPE_KEYWORDS, threshold = 6):
    keyword_count = sum(1 for keyword in keywords if keyword in chunk.lower())
    return keyword_count >= threshold 

def get_recipe_chunks(chunk):
    res = [] 
    for chunks in chunk:
        if is_recipe_chunk(chunks):
            res.append(chunks)
    return res