import requests
import json

API_KEY = "<YOUR_YELP_API_KEY>"
HEADERS = {"Authorization": "Bearer " + API_KEY}
Then, we can define a function that takes the user's location and interests as input and returns a list of recommended places:
def get_recommendations(location, interests):
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "location": location,
        "categories": "bars, distilleries",
        "attributes": interests,
        "sort_by": "rating",
        "limit": 10
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = json.loads(response.text)
    businesses = data.get("businesses", [])
    recommendations = []
    for business in businesses:
        name = business.get("name", "")
        rating = business.get("rating", "")
        address = ", ".join(business.get("location", {}).get("display_address", []))
        recommendations.append({"name": name, "rating": rating, "address": address})
    return recommendations
Finally, we can modify the get_bot_response function to call the get_recommendations function based on the user's input and return the recommendations as part of the AI response:
@app.route("/", methods=["POST"])
def get_bot_response():
    name = request.form.get("name")
    email = request.form.get("email")
    travel_from = request.form.get("travel_from")
    travel_to = request.form.get("travel_to")
    accommodation_type = request.form.get("accommodation_type")
    food_type = request.form.get("food_type")
    activity_type = request.form.get("activity_type")
    transportation_type = request.form.get("transportation_type")
    location = request.form.get("location")
    interests = request.form.get("interests")

    user_info = {
        "name": name,
        "contact_info": email,
        "travel_dates": {"from": travel_from, "to": travel_to},
        "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
        "itinerary": []
    }

    if location and interests:
        recommendations = get_recommendations(location, interests)
        ai_response = "Here are some local distilleries and cocktail bars you might be interested in:\n"
        for recommendation in recommendations:
            ai_response += f"{recommendation['name']} ({recommendation['rating']}/5)\n{recommendation['address']}\n\n"
    else:
        # Code for responding to user's non-recommendation related prompt
        ...

    # Retrieve the most recent previous response or set it to none
    ...