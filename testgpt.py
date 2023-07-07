import os 
import openai
import sys
from dotenv import load_dotenv, find_dotenv
from IPython.display import display, HTML
import requests
from bs4 import BeautifulSoup

url = "https://www.maangchi.com/recipe/gat-kimchi"
url = "https://www.allrecipes.com/recipe/20144/banana-banana-bread/"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")

#resultset item 
food_details = soup.find_all('script', {'type':'application/ld+json'})



load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

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
    You will be given a paragraph from a cooking website. \
    Extract the ingredients required for the recipe. \
    First extract the amount, then extract all ingredients, then extract other preparation details about the ingredient. \ 
    Output the result in an HTML format of unordered lists. Make sure to output every single ingredient in the paragraph. \
    Each unordered list should only have one ingredient listed.\
    The customer query will be delimited with {delimiter} characters.\
    
    Desired format: 
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
    
user_prompt = f"""
General tsos chicken served over a bowl of white rice
General Tso’s Chicken is a Chinese takeout go-to. Make it all in one dish in the comfort of your home for a sweet and spicy treat!
AD
Author: Natalya Drozhzhin
Course: Main Course
Cuisine: Asian
Keyword: general tsos chicken
Skill Level: Easy
Cost to Make: $10-$12
Calories: 386
Servings: 8 servings
Ingredients
2 lb chicken thighs, trimmed and cut into 1-inch pieces
1/2 cup corn starch
1/4 cup extra light olive oil, for frying, plus more as needed
2 tbsp minced ginger, from a 2-inch piece of ginger
3 cloves garlic, or 1 Tbsp grated or finely minced
1/2 tsp red pepper flakes, or added to taste
1 tsp sesame seeds, optional for garnish
General Tso's Sauce
1/2 cup cold water
5 tbsp low sodium soy sauce
3 tbsp rice vinegar, or more to taste
1 1/2 tbsp hoisin sauce
4 tbsp granulated sugar
1 1/2 tbsp cornstarch
"""
messages = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': f"{delimiter}{user_prompt}{delimiter}"}
]

response = get_completion_from_messages(messages)
print(response)
display(HTML(response))