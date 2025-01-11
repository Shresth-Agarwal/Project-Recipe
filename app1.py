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
    for recipe in data[:5]:  # Limit to first 5 recipes
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


if __name__ == "__main__":
    app.run(debug=True)
