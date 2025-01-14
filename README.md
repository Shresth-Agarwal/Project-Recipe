# Recipe API

This Flask-based API provides functionalities to search for recipes, retrieve recipe instructions, get nutritional information, find ingredient substitutes, convert ingredient quantities, and get random food trivia. The API interacts with the Spoonacular API for fetching data.

## Features

1. **Search Recipes**  
   Search for recipes using various filters such as ingredients, cuisine, diet, intolerances, and sorting options.

2. **Recipe Instructions**  
   Retrieve step-by-step instructions for a specific recipe by its ID.

3. **Nutritional Information**  
   Fetch nutritional information such as calories, protein, fat, carbohydrates, etc., for a specific recipe by its ID.

4. **Ingredient Substitutes**  
   Get a list of substitutes for a specific ingredient.

5. **Convert Ingredient Quantities**  
   Convert ingredient quantities between different units (e.g., cups to grams).

6. **Random Food Trivia**  
   Fetch a random food-related trivia.

---

## Endpoints

### 1. **Search Recipes**
   **URL:** `/search`  
   **Method:** `GET`  
   **Description:** Search for recipes using various filters.  
   **Query Parameters:**  
   - `query`: (optional) Search query string.
   - `ingredients`: (optional) Comma-separated list of ingredients.
   - `cuisine`: (optional) Cuisine type (e.g., Italian, Chinese). You can check the available cuisines [here](https://spoonacular.com/food-api/docs#Cuisines) 
   - `diet`: (optional) Diet type (e.g., vegetarian, keto). You can check available diets [here](https://spoonacular.com/food-api/docs#Diets)
   - `intolerances`: (optional) Comma-separated list of intolerances (e.g., gluten, dairy). You can check available intolerances [here](https://spoonacular.com/food-api/docs#Intolerances)
   - `sort`: (optional) Sort criteria (e.g., popularity, healthiness).
   - `page`: (optional) Page number for pagination (default: 1).
   - `page_size`: (optional) Number of results per page (default: 5).  

   **Response Example:**
   ```json
   {
       "recipes": [
           {"id": 123, "name": "Pasta", "image": "image_url"},
           {"id": 124, "name": "Pizza", "image": "image_url"}
       ]
   }
   ```

---

### 2. **Get Recipe Instructions**
   **URL:** `/recipe/<int:id>/instructions`  
   **Method:** `GET`  
   **Description:** Fetch step-by-step instructions for a recipe.  
   **Path Parameter:**  
   - `id`: Recipe ID.  

   **Response Example:**
   ```json
   {
       "instructions": [
           "1. Preheat the oven to 350°F.",
           "2. Mix ingredients.",
           "3. Bake for 25 minutes."
       ]
   }
   ```

---

### 3. **Get Nutritional Information**
   **URL:** `/recipe/<int:id>/nutritions`  
   **Method:** `GET`  
   **Description:** Get the nutritional details of a recipe.  
   **Path Parameter:**  
   - `id`: Recipe ID.  

   **Response Example:**
   ```json
   {
       "nutrition": [
           {"Calories": "200kcal"},
           {"Protein": "10g"}
       ]
   }
   ```

---

### 4. **Get Ingredient Substitutes**
   **URL:** `/substitute`  
   **Method:** `GET`  
   **Description:** Fetch substitutes for a specific ingredient.  
   **Query Parameter:**  
   - `ingredientName`: Name of the ingredient.  

   **Response Example:**
   ```json
   {
       "message": "No substitutes found",
       "substitutes": ["Greek Yogurt", "Coconut Cream"]
   }
   ```

---

### 5. **Convert Ingredient Quantities**
   **URL:** `/convert`  
   **Method:** `GET`  
   **Description:** Convert ingredient quantities between units.  
   **Query Parameters:**  
   - `ingredientName`: Name of the ingredient.
   - `sourceAmount`: Quantity to convert.
   - `sourceUnit`: (optional) Original unit (default: cups).
   - `targetUnit`: (optional) Target unit (default: grams).  

   **Response Example:**
   ```json
   {
       "converted": "200 grams"
   }
   ```

---

### 6. **Random Food Trivia**
   **URL:** `/trivia`  
   **Method:** `GET`  
   **Description:** Get a random food-related trivia.  

   **Response Example:**
   ```json
   {
       "Trivia": "Apples float because they are 25% air."
   }
   ```

---

## Error Handling

- Returns appropriate HTTP status codes and error messages for invalid inputs or API failures.  
- Example error response:  
  ```json
  {
      "error": "Page and page_size must be positive integers"
  }
  ```

---
