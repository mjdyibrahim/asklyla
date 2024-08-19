from flask import request, jsonify
import requests
import json
from app import app  # Import the app instance
from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com",
)

# Define a function to fetch the live music events based on the user's music preferences and location. You can use the Bandsintown API to fetch this information. Here is an example function:
def get_live_music_events(music_preferences, location):
    url = f"https://rest.bandsintown.com/v4/events?per_page=10&sort=date&location={location}&radius=25&only_recs=true&recommendations_based_on={music_preferences}&app_id=YOUR_APP_ID"

    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        return []
# Replace "YOUR_APP_ID" with your Bandsintown API app ID.

def get_openai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant who knows everything about music events.",
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return None

# Modify the get_bot_response() function to call the get_live_music_events() function and return the live music event suggestions to the user. Here is an example of how you can modify the function:
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
    music_preferences = request.form.get("music_preferences")
    location = request.form.get("location")

    user_info = {
        "name": name,
        "contact_info": email,
        "travel_dates": {"from": travel_from, "to": travel_to},
        "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
        "itinerary": []
    }

    # Get live music events based on the user's music preferences and location
    live_music_events = get_live_music_events(music_preferences, location)

    # Construct a message to the user with the live music event suggestions
    message = "Here are some live music events you might be interested in:\n\n"
    for event in live_music_events:
        message += f"{event['title']} on {event['datetime']} at {event['venue']['name']}\n"

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

    return jsonify({"message": message + "\n\n" + ai_response})
# With these modifications, the get_bot_response() function will now fetch live music events based on the user's music preferences and location and include them in the response to the user.