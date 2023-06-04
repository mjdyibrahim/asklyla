from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
import os
import requests

app = Flask(__name__)
openai.api_key = "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"
load_dotenv()

MINDBODY_API_KEY = os.getenv("MINDBODY_API_KEY")
MINDBODY_SITE_ID = os.getenv("MINDBODY_SITE_ID")
MINDBODY_ENDPOINT = "https://api.mindbodyonline.com/public/v6"

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

    user_info = {
        "name": name,
        "contact_info": email,
        "travel_dates": {"from": travel_from, "to": travel_to},
        "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
        "itinerary": []
    }

    user_response = request.json['message']
    ai_response = ""

    # Retrieve the most recent previous response or set it to none
    if len(previous_responses) > 0:
        previous_response = previous_responses[-1]
        prompt = [
            {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need."},
            {"role": "user", "content": previous_response['user']},
            {"role": "assistant", "content": previous_response['assistant']},
            {"role": "user", "content": user_response}
        ]
    else:
        prompt = [
            {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need."},
            {"role": "user", "content": ""},
            {"role": "assistant", "content": "Hi, I'm Lyla, your personal travel companion! Before we start, can you tell me your name?"},
            {"role": "user", "content": user_response}
        ]

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=300,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )

    ai_response = response.choices[0].text.strip()

    if "spa" in user_response or "wellness" in user_response:
        # Use MindBody API to search for local spa and wellness services
        try:
            search_params = {
                "SearchText": "spa",
                "Location": {
                    "Latitude": 37.7749,
                    "Longitude": -122.4194,
                    "Distance": 10,
                    "PostalCode": "94103",
                    "CountryCode": "US"
                },
                "Fields": ["BusinessId", "BusinessName", "Address"],
                "OnlineOnly": False,
                "SchedulingWindow": {
                    "StartDateTime": "2022-01-01T00:00:00",
                    "EndDateTime": "2022-12-31T00:00:00"
                }
            }
            headers = {"Api-Key": MINDBODY_API_KEY, "SiteId": MINDBODY_SITE_ID}
            r = requests.post(f"{MINDBODY_ENDPOINT}/finder/search", json=search_params, headers=headers)
            if r.status_code == 200:
                results = r.json().get("Businesses", [])
                if len(results) > 0:
                    ai_response += "\n\nHere are some local spa and wellness services I found:\n"
                    for result in results:
                        ai_response += f"\n- {result['BusinessName']}, located at {result['Address']['AddressLine1']}, {result['Address']['City']}, {result['Address']['State']}, {result['Address']['PostalCode']}"
                else:
                    ai_response += "\n\nSorry, I couldn't find any local spa and wellness services."
            else:
                ai_response += "\n\nSorry, there was an error while searching for local spa and wellness services. Please try again later."
        except:
            ai_response += "\n\nSorry, there was an error while searching for local spa and wellness services. Please try again later."

    previous_response = {"user": user_response, "assistant": ai_response}
    previous_responses.append(previous_response)

    return jsonify({"message": ai_response})

if __name__ == "__main__":
    app.run()