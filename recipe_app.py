from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)

key = "565dbcc40da44ae086ecdf610570f7eb"


@app.route('/search_recipes', methods=["GET"])
def get_recipe():
    # Get ingredients from query parameters
    ingredients = request.args.get('ingredients')
    if not ingredients:
        return jsonify({'error': 'No ingredients provided'}), 400

    # Construct the Spoonacular API URL
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&apiKey={key}"
    response = requests.get(url)

    # Handle API errors
    if response.status_code != 200:
        return jsonify({'error': 'Could not load recipes'}), response.status_code

    # Parse the response JSON
    data = response.json()
    if not data:
        return jsonify({'error': 'No recipes found'}), 404

    # Collect recipe details in a list
    recipes = []
    for recipe in data[:10]:  # Limit to first 5 recipes
        recipes.append({
            'id': recipe['id'],
            'name': recipe['title']
        })

    return jsonify({'recipes': recipes})


@app.route('/recipe/<int:id>/instructions', methods=["GET"])
def get_instructions(id):
    if not id:
        return jsonify({"ERROR": "Couldn't locate the recipe id"})

    url = f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions?apiKey={key}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"ERROR": "Coudn't fetch the recipe instructions"}), response.status_code
    data = response.json()
    instructions = []
    steps = data[0]['steps']
    for step in steps:
        instructions.append(f'{step['number']}. {step['step']} ')
    return jsonify({'Instuctions': instructions})


@app.route('/recipe/<int:id>/nutritions')
def get_nutrients(id):
    if not id:
        return jsonify({"Error": "Couldn't find the recipe"})
    url = f'https://api.spoonacular.com/recipes/{id}/nutritionWidget.json?apiKey={key}'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'Error': 'Couldnt fetch nutrition data for the recipe'}), response.status_code
    data = response.json()
    req_n = ['Calories', 'Fat', 'Carbohydrates', 'Sugar', 'Cholesterol', 'Protein', 'Iron', 'Calcium', 'Fiber']
    req_v = ['Vitamin A', 'Vitamin B1', 'Vitamin B2', 'Vitamin B3', 'Vitamin B5', 'Vitamin B6', 'Vitamin B12', 'Vitamin E', 'Vitamin K']
    nutrition = []
    vitamins = []
    for nutrient in data['nutrients']:
        if nutrient['name'] in req_n:
            nutrition.append({nutrient['name']: str(nutrient['amount']) + nutrient['unit']})
        elif nutrient['name'] in req_v:
            vitamins.append({nutrient['name']: str(nutrient['amount']) + nutrient['unit']})
    nutrition.extend(vitamins)
    return jsonify(nutrition)


@app.route('/complex_search')
def complex_search(query=None, ingredients=None, cuisine=None, diet=None, intolerances=None, max_ready_time=None, sort=None):
    params = {
        "query": query,
        "includeIngredients": ','.join(ingredients) if ingredients else None,
        "cuisine": cuisine,
        "diet": diet,
        "intolerances": ','.join(intolerances) if intolerances else None,
        "maxReadyTime": max_ready_time,
        "sort": sort,
        "number": 10
    }
    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={key}'
    results = requests.get(url, params=params)
    if results.status_code != 200:
        return jsonify({'error': 'Could not load recipes'}), results.status_code
    data = results.json()
    data = data['results']
    recipes = []
    for result in data:
        recipes.append([result['image'], {'Id': result['id'], 'Name': result['title']}])
    return jsonify(recipes)


@app.route('/search')
def search():
    query = request.args.get('query', default=None)
    ingredients = request.args.get('ingredients', default=None)
    cuisine = request.args.get('cuisine', default=None)
    diet = request.args.get('diet', default=None)
    intolerances = request.args.get('intolerances', default=None)
    max_ready_time = request.args.get('max_ready_time', default=None, type=int)
    sort = request.args.get('sort', default=None)
    return complex_search(query, ingredients, cuisine, diet, intolerances, max_ready_time, sort)


if __name__ == "__main__":
    app.run(debug=True)
