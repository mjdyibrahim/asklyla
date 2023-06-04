import requests
import json
# Create a function to get the coffee shops based on the user's location and preferences:
def get_coffee_shops(location, preferences):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": "Bearer <your Yelp API key>"
    }
    params = {
        "term": "coffee",
        "location": location,
        "categories": "coffee,cafes",
        "price": preferences["price"],
        "rating": preferences["rating"],
        "sort_by": "rating"
    }
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)
    return data["businesses"]

# Modify the get_bot_response function to call the get_coffee_shops function and return the coffee shop recommendations to the user:
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
    preferences = {
        "price": request.form.get("price"),
        "rating": request.form.get("rating")
    }
    
    user_info = {
        "name": name,
        "contact_info": email,
        "travel_dates": {"from": travel_from, "to": travel_to},
        "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
        "itinerary": []
    }
    
    # Call the get_coffee_shops function to get the coffee shop recommendations
    coffee_shops = get_coffee_shops(location, preferences)
    
    # Add code to display the coffee shop recommendations to the user
    recommendation = "Here are some coffee shops and cafes you might like:\n\n"
    for shop in coffee_shops:
        recommendation += "- " + shop["name"] + " (" + shop["rating"] + " stars)\n"
    recommendation += "\nEnjoy your coffee!"
    
    # Retrieve the most recent previous response or set it to none
    if len(previous_responses) == 0:
        user_response = request.json['message']
        ai_response = ""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need."},
                {"role": "user", "content": ""},
                {"role": "assistant", "content": "Hi, I'm Lyla, your personal travel companion! Before we start, can you tell me your name?"},
                {"role": "user", "content": user_response}
            ],
            temperature=0.7,
            max_tokens=300,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_response = response.choices[0].message["content"].strip()
    else:
        previous_response = previous_responses[-1]
        user_response = request.json['message']
        prompt = [
            {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need."},
            {"role": "user", "content": previous_response['user']},
            {"role": "assistant", "content": previous_response['assistant']},
            {"role": "user", "content": user_response}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.7,
            max_tokens=300,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_response = response.choices[0].message["content"].strip()
        
        previous_response = {"user": user_response, "assistant": ai_response}
    previous_responses.append(previous_response)
    
    return jsonify({"message": ai_response + "\n\n" + recommendation})
# Note: Replace <your Yelp API key> with your actual Yelp API key.