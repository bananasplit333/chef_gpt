import json
import os 
import openai
from dotenv import load_dotenv, find_dotenv
from IPython.display import display, HTML
import requests
from bs4 import BeautifulSoup

#
urls = [
    "https://www.vkusnyblog.com/recipe/myatnyj-limonad/",
    "https://www.allrecipes.com/recipe/20144/banana-banana-bread/",
    "https://www.bonappetit.com/recipe/pork-shoulder-inasal",
    "https://www.simplyrecipes.com/lamb-skewers-with-haitian-epis-5225102",
    "https://www.maangchi.com/recipe/gat-kimchi", 
    "https://www.errenskitchen.com/chinese-chicken-broccoli/",
    "https://thewoksoflife.com/kung-pao-chicken/",
    "https://www.bonappetit.com/recipe/pork-shoulder-inasal",
    "https://www.foodnetwork.com/recipes/food-network-kitchen/slow-cooker-chicken-noodle-soup-3364248 "
]


load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']



#extract json-ld from page, convert to dict
def get_ingredients(url:str) -> dict: 
    parser="html.parser"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    res=requests.get(url, headers=headers)
    soup=BeautifulSoup(res.text, parser)
    script_tag = soup.find("script", {"type": "application/ld+json"})
    if script_tag:
        metadata= json.loads("".join(script_tag.contents))
        return parse_dictionary(metadata)
    else:
       raise Exception("no script tag found")

#return the list of ingredients from the dict
def parse_dictionary(items) -> list:
    ingredients = []
    if isinstance(items, dict):
       if "recipeIngredient" in items:
           ingredients = items["recipeIngredient"]
       else:
           for key, value in items.items():
               if isinstance(value, (dict, list)):
                   ingredients.extend(parse_dictionary(value))
    elif isinstance(items, list):
        for item in items:
            if isinstance(item, (dict,list)):
                ingredients.extend(parse_dictionary(item))
    return ingredients

def get_completion_from_messages(
    messages,
    model="gpt-3.5-turbo",
    temperature = 0,
    max_tokens = 500,
):
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens,
    )
    return response.choices[0].message["content"]

delimiter = "####"
system_message=f"""
    You will be given a paragraph from a cooking blog. \
    Extract the ingredients required for the recipe. \
    First extract the amount, then extract all ingredients, then extract other preparation details about the ingredient. \ 
    Output the result in an HTML format of unordered lists. Make sure to output every single ingredient in the paragraph. \
    Each unordered list should only have one ingredient listed.\
    The customer query will be delimited with {delimiter} characters.\
    
    Desired format:
    Name of Dish 
    <amount>: tablespoon, teaspoon should be abbreviated to tbsp and tsp. Convert every imperial measurement to metric (except volume).
    <ingredient name> is concise and does not contain extra details. 
    <preparation details> has a concise, brief description about the ingredient. For example, "onion finely chopped and diced" would equate to something like "onion, fine dice"

    <amount > <ingredient name>, <(preparation details)>
    <amount>, <ingredient name>, <(preparation details)>
    <amount>, <ingredient name>, <(preparation details)>
    ...

    Remove any trailing commas 

    If amount is of count, remove the comma proceeding it.
    Do not include brackets. Only output one measurement of each ingredient.
    """
    
print("Welcome to the recipe parser!")
for url in urls:
    user_prompt = get_ingredients(url)
    messages = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': f"{delimiter}{user_prompt}{delimiter}"}
    ]
    response = get_completion_from_messages(messages)
    display(HTML(response))
    print(response)
#response = get_completion_from_messages(messages)
#print(response)
#display(HTML(response))