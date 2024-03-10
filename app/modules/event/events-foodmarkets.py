from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv 
import openai import os 
import requests

app = Flask(name)

openai.api_key = "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"

# List to store previous responses
previous_responses = []

# API key for food-related activities
food_api_key = "your_api_key_here"

@app.route("/") 
def home(): 
    return render_template("index.html")

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

user_info = {
    "name": name,
    "contact_info": email,
    "travel_dates": {"from": travel_from, "to": travel_to},
    "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
    "itinerary": []
}

if 'food' in food_type:
    # Get user location using IP address
    ip_address = request.remote_addr
    location_url = f"http://ip-api.com/json/{ip_address}"
    location_response = requests.get(location_url).json()
    latitude = location_response['lat']
    longitude = location_response['lon']

    # Use food API to get nearby food markets and experiences
    food_url = f"https://api.yelp.com/v3/businesses/search?latitude={latitude}&longitude={longitude}&categories=food&sort_by=rating&limit=3"
    headers = {
        "Authorization": f"Bearer {food_api_key}",
        "Content-Type": "application/json"
    }
    food_response = requests.get(food_url, headers=headers).json()

    # Format response with top 3 food markets and experiences
    food_recommendation = "Here are some top food markets and experiences near you:\n"
    for i, business in enumerate(food_response['businesses']):
        food_recommendation += f"{i+1}. {business['name']} ({business['location']['address1']})\n"
    ai_response = food_recommendation
else:
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

        # Save previous response
        previous_response = {"user": user_response, "assistant": ai_response}
        previous_responses.append(previous_response)

return jsonify({"message": ai_response})

if name == "main": 
    app.run()