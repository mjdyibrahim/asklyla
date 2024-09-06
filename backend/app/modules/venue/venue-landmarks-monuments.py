
from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv 
import openai 
import os 
import requests

app = Flask(name) openai.api_key = "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" 
load_dotenv()

List to store previous responses
previous_responses = []

Google Places API key
places_api_key = os.getenv("PLACES_API_KEY")

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

# Retrieve the most recent previous response or set it to none
if len(previous_responses) == 0:
    user_response = request.json['message']
    ai_response = ""
    response = openai.ChatCompletion.create(
        model="text-davinci-002",
        prompt="You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itinerary based on their preferences and personality, objectives and current life circumstances and help them book all the services they need.\n\nHi, I'm Lyla, your personal travel companion! Before we start, can you tell me your name?",
        temperature=0.7,
        max_tokens=300,
        frequency_penalty=0,
        presence_penalty=0
    )
    ai_response = response.choices[0].text.strip()
else:
    previous_response = previous_responses[-1]
    user_response = request.json['message']
    prompt = [
        {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itinerary based on their preferences and personality, objectives and current life circumstances and help them book all the services they need."},
        {"role": "user", "content": previous_response['user']},
        {"role": "assistant", "content": previous_response['assistant']},
        {"role": "user", "content": user_response}
    ]
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=300,
        frequency_penalty=0,
        presence_penalty=0
    )
    ai_response = response.choices[0].text.strip()

# Suggest local historical landmarks and monuments
if 'historical landmarks' in user_response or 'monuments' in user_response:
    location = user_info['travel_to']
    radius = 10000
    types = 'tourist_attraction'
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={places_api_key}&location={location}&radius={radius}&types={types}'
    response = requests.get(url)
    data = response.json()
    if len(data['results']) == 0:
        ai_response += "\n\nSorry, I couldn't find any historical landmarks or monuments near your destination."
    else:
        ai_response += "\n\nHere are some historical landmarks and monuments you might be interested in:\n"
        for result in data['results']:
            ai_response += f"\n{result['name']} - {result['vicinity']}"

previous_response = {"user": user_response, "assistant": ai_response}
previous_responses.append(previous_response)

return jsonify({"message": ai_response})
if name == "main": 
    app.run()