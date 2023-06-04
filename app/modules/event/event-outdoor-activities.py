from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv 
import openai 
import os 
import requests

app = Flask(name) openai.api_key = "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" load_dotenv()

# List to store previous responses
previous_responses = []

# AllTrails API key
alltrails_key = os.getenv("ALLTRAILS_API_KEY")

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

if activity_type == "Outdoor":
    # Get nearby trails from AllTrails API
    url = f"https://www.alltrails.com/api/2/search/?key={alltrails_key}&q=hiking&lat={location['lat']}&lon={location['lng']}"
    response = requests.get(url)
    trails = response.json()["places"]

    # Get top 3 trails based on user's preference
    top_trails = []
    for trail in trails:
        if trail["activity_type_name"] == activity_type and trail["rating"] >= 4:
            top_trails.append(trail)
        if len(top_trails) == 3:
            break

    # Create a response message with trail recommendations
    response_message = "Here are some nearby trails you might like:\n"
    for trail in top_trails:
        response_message += f"{trail['name']} - {trail['city']}, {trail['state']}\n"

else:
    # Retrieve the most recent previous response or set it to none
    if len(previous_responses) == 0:
        user_response = request.json['message']
        ai_response = ""
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itinerary based on their preferences and personality, objectives, and current life circumstances and help them book all the services they need.\n\nUser: {user_response}\nLyla:",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        ai_response = response.choices[0].text.strip()

    else:
        previous_response = previous_responses[-1]
        user_response = request.json['message']
        prompt = f"You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itinerary based on their preferences and personality, objectives, and current life circumstances and help them book all the services they need.\n\nUser: {previous_response['user']}\nLyla: {previous_response['assistant']}\n\nUser: {user_response}\nLyla:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        ai_response = response.choices[0].text.strip()

        previous_response = {"user": user_response, "assistant": ai_response}
        previous_responses.append(previous_response)

return jsonify({"message": ai_response})