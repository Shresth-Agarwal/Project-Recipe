from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

API_KEY = "565dbcc40da44ae086ecdf610570f7eb"


@app.route('/search', methods=["GET"])
def search():
    # Extract query parameters
    query = request.args.get('query', default=None)
    ingredients = request.args.get('ingredients', default=None)
    cuisine = request.args.get('cuisine', default=None)
    diet = request.args.get('diet', default=None)
    intolerances = request.args.get('intolerances', default=None)
    sort = request.args.get('sort', default=None)

    # Pagination parameters
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=5, type=int)

    if page < 1 or page_size < 1:
        return jsonify({"error": "Page and page_size must be positive integers"}), 400

    # Calculate offset
    offset = (page - 1) * page_size

    # Construct parameters for complex search
    params = {
        "query": query,
        "includeIngredients": ingredients,
        "cuisine": cuisine,
        "diet": diet,
        "intolerances": intolerances,
        "sort": sort,
        "apiKey": API_KEY,
        "number": page_size,
        "offset": offset,
    }

    # Remove None values from params
    params = {key: value for key, value in params.items() if value is not None}

    # Call Spoonacular's complex search API
    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}'
    response = requests.get(url, params=params)

    # Handle API errors
    if response.status_code != 200:
        return jsonify({'error': 'Could not load recipes'}), response.status_code

    # Parse and process the response JSON
    data = response.json().get('results', [])
    recipes = [{'id': recipe['id'], 'name': recipe['title'], 'image': recipe['image']} for recipe in data]
    if len(recipes) == 0:
        return jsonify({"Error": "No more recipes found"})

    return jsonify({"recipes": recipes})


# Endpoint to get instructions for a recipe by ID
@app.route('/recipe/<int:id>/instructions', methods=["GET"])
def get_instructions(id):
    # Construct the Spoonacular API URL for instructions
    url = f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions?apiKey={API_KEY}"
    response = requests.get(url)

    # Handle API errors
    if response.status_code != 200:
        return jsonify({"error": "Could not fetch recipe instructions"}), response.status_code

    # Parse and process the response JSON
    data = response.json()
    if not data or 'steps' not in data[0]:
        return jsonify({"error": "No instructions found"}), 404

    # Extract steps from the instructions
    steps = data[0]['steps']
    instructions = [f"{step['number']}. {step['step']}" for step in steps]

    return jsonify({'instructions': instructions})


# Endpoint to get nutritional information for a recipe by ID
@app.route('/recipe/<int:id>/nutritions', methods=["GET"])
def get_nutrients(id):
    # Construct the Spoonacular API URL for nutrition
    url = f'https://api.spoonacular.com/recipes/{id}/nutritionWidget.json?apiKey={API_KEY}'
    response = requests.get(url)

    # Handle API errors
    if response.status_code != 200:
        return jsonify({'error': 'Could not fetch nutrition data'}), response.status_code

    # Parse and process the response JSON
    data = response.json()
    if not data:
        return jsonify({'error': 'No nutrition data found'}), 404

    # Extract specific nutrition information
    required_nutrients = ['Calories', 'Fat', 'Carbohydrates', 'Sugar', 'Cholesterol', 'Protein', 'Iron', 'Calcium', 'Fiber']
    nutrition = [{nutrient['name']: f"{nutrient['amount']}{nutrient['unit']}"} for nutrient in data['nutrients'] if nutrient['name'] in required_nutrients]

    return jsonify({'nutrition': nutrition})


# Endpoint to get substitutes for an ingredient
@app.route('/substitute', methods=["GET"])
def get_substitute():
    # Get ingredient name from query parameters
    ingredient = request.args.get('ingredientName')
    if not ingredient:
        return jsonify({'error': 'No ingredient name provided'}), 400

    # Construct the Spoonacular API URL for ingredient substitutes
    url = f"https://api.spoonacular.com/food/ingredients/substitutes?ingredientName={ingredient}&apiKey={API_KEY}"
    response = requests.get(url)

    # Handle API errors
    if response.status_code != 200:
        return jsonify({'error': 'Could not fetch substitutes'}), response.status_code

    # Parse and process the response JSON
    data = response.json()
    substitutes = {
        'message': data.get('message', 'No message available'),
        'substitutes': data.get('substitutes', [])
    }

    return jsonify(substitutes)


# Endpoint to convert amounts into grams and cups
@app.route('/convert', methods=['GET'])
def convert():
    # Get the arguments for url request
    ingredient = request.args.get('ingredientName')
    sourceAmount = request.args.get('sourceAmount')
    sourceUnit = request.args.get('sourceUnit', default='cups')
    targetUnit = request.args.get('targetUnit', default='grams')

    # Return error if the required arguments are not provided
    if not ingredient or not sourceAmount:
        return jsonify({'Error': 'Ingredient name or source amount not specified'})

    url = f'https://api.spoonacular.com/recipes/convert?apiKey={API_KEY}&ingredientName={ingredient}&sourceAmount={sourceAmount}&sourceUnit={sourceUnit}&targetUnit={targetUnit}'
    response = requests.get(url)

    # Return error if response is not fetched properly
    if response.status_code != 200:
        return jsonify({'Error': 'Couldn\'t fetch the converted amount'}), response.status_code

    # Return only the converted amount
    data = response.json()
    return jsonify(str(data['targetAmount']) + " " + data['targetUnit'])


# Function to return a simple food related trivia
@app.route('/trivia', methods=['GET'])
def trivia():
    url = f'https://api.spoonacular.com/food/trivia/random?apiKey={API_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'Error': 'Coudn\'t retrieve food trivia'})

    data = response.json()
    return jsonify({'Trivia': data['text']})


if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode
