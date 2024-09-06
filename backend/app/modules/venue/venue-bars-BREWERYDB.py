from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv 
import openai import os 
import requests

app = Flask(name) 

openai.api_key = "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" 
load_dotenv()

# BreweryDB API key
BREWERYDB_API_KEY = os.getenv("BREWERYDB_API_KEY")

# List to store previous responses
previous_responses = []

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
    location = request.form.get("location")

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

    # Suggest local craft breweries and beer bars
    if 'beer' in user_response.lower():
        url = f"https://api.brewerydb.com/v2/search?q=beer&type=brewery&key={BREWERYDB_API_KEY}&location={location}"
        response = requests.get(url)
        data = response.json()

        if data['data']:
            brewery = data['data'][0]['brewery']
            brewery_name = brewery['name']
            brewery_url = brewery['website']
            brewery_city = brewery['locations'][0]['locality']
            brewery_state = brewery['locations'][0]['region']

            ai_response += f"\n\nI found a local brewery you might enjoy! Check out {brewery_name} in {brewery_city}, {brewery_state}. Here's the website: {brewery_url}"
        else:
            ai_response += "\n\nI couldn't find any local breweries or beer bars. Sorry about that!"

previous_response = {"user": user_response, "assistant": ai_response}
previous_responses.append(previous_response)

return jsonify({"message": ai_response})

if name == "main": 
    app.run()

# Note: In this code, we assume that the user provides their location in the form. The location is used to search for local breweries and beer bars using the BreweryDB API. If no results are found, the code returns a message apologizing for not being able to find any local breweries or beer bars.

