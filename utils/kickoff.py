import json
from .data_parser import extract_text_from_url, extract_recipe_ingredients, extract_instructions

def kickoff(url):
    recipe_json = extract_text_from_url(url)
    data_obj = {'ingredients':extract_recipe_ingredients(recipe_json), 'cooking_instructions':extract_instructions(recipe_json)}
    print('ingredients')
    ingredients = json.loads(data_obj['ingredients'])['ingredients']
    for item in ingredients:
        print(item)


    print('instructions')
    instructions = json.loads(data_obj['cooking_instructions'])['cooking_instructions']
    for task in instructions:
        print(task)
