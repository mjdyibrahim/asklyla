from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/api/cityguide', methods=['GET'])
def city_guide():
    city_name = request.args.get('city')

    if city_name:
        print(f"Received city name: {city_name}")

        # Read data from cities.json
        with open('cities.json', 'r') as json_file:
            cities_data = json.load(json_file)

        city_data = None
        for city in cities_data:
            if city['name'].lower() == city_name.lower():
                city_data = city
                break

        if city_data:
            return jsonify(city_data)
        else:
            return jsonify({"error": "City not found"}), 404

    return jsonify({"error": "No city specified"}), 400

@app.route('/api/cairo.json', methods=['GET'])
def cairo_data():
    with open('cairo.json', 'r') as json_file:
        cairo_data = json.load(json_file)
    return jsonify(cairo_data)

if __name__ == '__main__':
    app.run(debug=True)
