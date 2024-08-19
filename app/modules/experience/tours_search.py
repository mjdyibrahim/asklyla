from flask import Blueprint, request, jsonify
import requests

# Viator API endpoint and API key
VIATOR_API_ENDPOINT = "https://api.viator.com/v2"
VIATOR_API_KEY = "your_api_key_here"

# GetYourGuide API endpoint and API key
GETYOURGUIDE_API_ENDPOINT = "https://api.getyourguide.com/2"
GETYOURGUIDE_API_KEY = "your_api_key_here"

tours_bp = Blueprint('tours', __name__)

@tours_bp.route("/search_tours", methods=["GET"])
def search_tours():
    location = request.args.get("location")
    date = request.args.get("date")
    category = request.args.get("category")

    # Search tours on Viator
    viator_url = f"{VIATOR_API_ENDPOINT}/search?apiKey={VIATOR_API_KEY}&destId={location}&topX=10&startDate={date}&categoryId={category}"
    viator_response = requests.get(viator_url).json()
    viator_tours = viator_response.get("data", {}).get("results", [])

    # Search tours on GetYourGuide
    getyourguide_url = f"{GETYOURGUIDE_API_ENDPOINT}/activities?limit=10&offset=0&place_ids={location}&categories={category}&start_date={date}&page_size=10&order_by=popularity:desc&client_id={GETYOURGUIDE_API_KEY}"
    getyourguide_response = requests.get(getyourguide_url).json()
    getyourguide_tours = getyourguide_response.get("data", {}).get("activities", [])

    # Combine and format the tour data
    tours = []
    for tour in viator_tours:
        tours.append({
            "title": tour.get("title"),
            "description": tour.get("description"),
            "price": tour.get("price", {}).get("formattedPrice"),
            "image_url": tour.get("imageURL"),
            "vendor": "Viator"
        })
    for tour in getyourguide_tours:
        tours.append({
            "title": tour.get("title"),
            "description": tour.get("description"),
            "price": tour.get("price", {}).get("value"),
            "image_url": tour.get("images", [])[0].get("url"),
            "vendor": "GetYourGuide"
        })

    return jsonify({"tours": tours})