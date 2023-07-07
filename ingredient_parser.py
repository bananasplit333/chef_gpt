import requests
from bs4 import BeautifulSoup
import json

#url = "https://www.foodnetwork.com/recipes/rachael-ray/caprese-salad-recipe-1939232"
#url = "https://www.walderwellness.com/tastes-like-summer-salad-with-fresh-local-ingredients/"
url = "https://www.maangchi.com/recipe/gat-kimchi"
#url = "https://www.allrecipes.com/recipe/20144/banana-banana-bread/"
#url = "https://sweetandsavorymeals.com/korean-beef-bulgogi/"

def get_ingredients(url="https://www.maangchi.com/recipe/gat-kimchi"):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    #find the json file:  
    food_details = soup.find('script', {'type':'application/ld+json'}).string
    json_data = json.loads(food_details)
    if (json_data[0].get('recipeIngredient')):
        return json_data[0].get('recipeIngredient')
    else:
        return json_data["@graph"][0].get('recipeIngredient')
    

print(get_ingredients(url))