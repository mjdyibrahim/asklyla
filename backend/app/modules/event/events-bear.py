from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv 
import openai 
import os 
import requests

app = Flask(name) openai.api_key = "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"

# List to store previous responses
previous_responses = []

# Third-party API endpoints
BREWERY_API_URL = "https://api.openbrewerydb.org/breweries" BEER_API_URL = "https://api.punkapi.com/v2/beers"

@app.route("/") 
def home(): 
    return render_template("index.html")

@app.route("/", methods=["POST"]) def get_bot_response(): name = request.form.get("name") email = request.form.get("email") travel_from = request.form.get("travel_from") travel_to = request.form.get("travel_to") accommodation_type = request.form.get("accommodation_type") food_type = request.form.get("food_type") activity_type = request.form.get("activity_type") transportation_type = request.form.get("transportation_type")

user_info = { 
    "name": name, 
    "contact_info": email, 
    "travel_dates": {"from": travel_from, "to": travel_to}, 
    "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type}, 
    "itinerary": [] 
} 

# Check if the user wants to find local breweries and beer tastings 
if 'beer' in request.json['message'] or 'brewery' in request.json['message']: 
    user_location = request.form.get("location") 
    brewery_type = request.form.get("brewery_type") 
    beer_type = request.form.get("beer_type") 
    
    # Make API requests to get relevant information based on user's preferences and location 
    brewery_response = requests.get(f"{BREWERY_API_URL}?by_city={user_location}&by_type={brewery_type}") 
    beer_response = requests.get(f"{BEER_API_URL}?beer_name={beer_type}") 
    
    # Parse the responses and extract relevant information 
    breweries = [b["name"] for b in brewery_response.json()] 
    beers = [b["name"] for b in beer_response.json()] 
    
    # Generate a response to suggest local breweries and beer tastings 
    if len(breweries) > 0 and len(beers) > 0: 
        ai_response = f"I found these local breweries that might interest you: {', '.join(breweries)}. And you might want to try these beers: {', '.join(beers)}." 
    elif len(breweries) > 0: 
        ai_response = f"I found these local breweries that might interest you: {', '.join(breweries)}." 
    elif len(beers) > 0: 
        ai_response = f"You might want to try these beers: {', '.join(beers)}." 
    else: 
        ai_response = "Sorry, I couldn't find any local breweries or beer tastings that match your preferences." 
    
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
        
        previous_response = {"user": user_response, "assistant": ai_response} 
        
    previous_responses.append(previous_response) 

return jsonify({"message": ai_response}) 
if name == "main": 
    app.run()


    
import requests

@app.route("/recommendations", methods=["POST"]) 
def get_recommendations(): # Get user's location and interests 
    location = request.form.get("location") 
    interests = request.form.get("interests")

# Fetch recommendations from Untappd API
url = f"https://api.untappd.com/v4/search/beer?q={interests}&limit=10&lat={location['lat']}&lng={location['lng']}&radius=10"
response = requests.get(url, headers={"Authorization": "Bearer <YOUR_API_KEY>"})

# Parse the response and send back the recommendations to the user
recommendations = []
for item in response.json()["response"]["beers"]["items"]:
    brewery = item["brewery"]["brewery_name"]
    beer = item["beer_name"]
    recommendations.append(f"{beer} from {brewery}")
return jsonify({"recommendations": recommendations})
This code defines a new route "/recommendations" that accepts the user's location and interests as inputs. It then uses the Untappd API to fetch beer recommendations based on the user's location and interests. Finally, it formats the recommendations and sends them back to the user as a JSON response.
