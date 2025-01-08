from flask import Flask, jsonify, request
import requests
from flask_cors import CORS  # type: ignore

app = Flask(__name__)
CORS(app)

key = "bedd24b87476b717c33c3cf7b73c0a71"


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'Error': 'City name is required'}), 400

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'Error': 'City name not found'}), 404

    data = response.json()
    info = {
        'City': data['name'],
        'temperature': data['main']['temp'],
        'Description': data['weather'][0]['description']
    }
    return jsonify(info)


if __name__ == "__main__":
    app.run(debug=True)
