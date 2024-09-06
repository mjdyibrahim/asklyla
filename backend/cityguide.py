from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/cityguide', methods=['POST', 'GET'])
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
            city_guide_content = render_template('cityguide.html', city=city_data)
            return city_guide_content
        else:
            return render_template('cityguide.html')

    return render_template('cityguide.html')

if __name__ == '__main__':
    app.run(debug=True)
