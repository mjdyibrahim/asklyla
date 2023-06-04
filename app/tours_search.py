import requests

Viator API endpoint and API key
VIATOR_API_ENDPOINT = "https://api.viator.com/v2" VIATOR_API_KEY = "your_api_key_here"

GetYourGuide API endpoint and API key
GETYOURGUIDE_API_ENDPOINT = "https://api.getyourguide.com/2" GETYOURGUIDE_API_KEY = "your_api_key_here"

@app.route("/search_tours", methods=["GET"]) def search_tours(): location = request.args.get("location") date = request.args.get("date") category = request.args.get("category")

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
This code defines a new route "/search_tours" that accepts GET requests with parameters for location, date, and category. It then uses the APIs of Viator and GetYourGuide to search for tours and activities that match the given parameters, and combines the results in a standardized format. The code can be further extended to allow users to book tours and activities directly through the app using the APIs of the respective platforms.

