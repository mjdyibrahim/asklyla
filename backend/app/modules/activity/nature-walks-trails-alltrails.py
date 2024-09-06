from flask import Blueprint, request, jsonify
from alltrails import Client
from geopy.geocoders import Nominatim
import requests

nature_walks_bp = Blueprint('nature_walks', __name__)

@nature_walks_bp.route("/suggested_trails", methods=["POST"])
def suggested_trails():
    fitness_level = request.form.get("fitness_level")
    location = request.form.get("location")

    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(location)
    latitude, longitude = location.latitude, location.longitude

    client = Client(api_key="your_api_key_here")
    trails = client.get_trails_by_coordinates(latitude, longitude, max_distance=10, max_results=10, min_difficulty=fitness_level)

    response = [{"name": trail.name, "location": trail.location, "difficulty": trail.difficulty} for trail in trails]
    return jsonify(response)

# Function to handle bot responses related to trail suggestions
def get_trail_suggestions(user_info):
    response = requests.post('http://localhost:5000/suggested_trails', 
                             data={'fitness_level': user_info['preferences']['fitness_level'], 
                                   'location': user_info['travel_dates']['to']})
    suggested_trails = response.json()
    # Add code to format and return the suggested trails to the user
    return suggested_trails

# ... any other related functions ...