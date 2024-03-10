
from flask import Flask, render_template, request, jsonify 
from dotenv import load_dotenv 
import openai 
import os 
import requests

app = Flask(name)

openai.api_key = "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"

List to store previous responses
previous_responses = []

Third-party API key for art gallery recommendations
art_api_key = os.getenv("ART_API_KEY")

@app.route("/") def home(): return render_template("index.html")

@app.route("/", methods=["POST"]) def get_bot_response(): name = request.form.get("name") email = request.form.get("email") travel_from = request.form.get("travel_from") travel_to = request.form.get("travel_to") accommodation_type = request.form.get("accommodation_type") food_type = request.form.get("food_type") activity_type = request.form.get("activity_type") transportation_type = request.form.get("transportation_type") location = request.form.get("location") interest = request.form.get("interest")

user_info = {
    "name": name,
    "contact_info": email,
    "travel_dates": {"from": travel_from, "to": travel_to},
    "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
    "itinerary": []
}

if interest.lower() == "art":
    # Get art gallery recommendations based on user's location using third-party API
    art_response = requests.get(f"https://api.art.com/art-gallery/v1/galleries?apiKey={art_api_key}&location={location}&pageNum=1&pageSize=5")
    galleries = art_response.json()["galleries"]
    gallery_names = [gallery["galleryName"] for gallery in galleries]

    # Build AI response with gallery recommendations
    ai_response = f"Here are some art galleries in {location} you might be interested in:\n"
    for gallery in gallery_names:
        ai_response += f"- {gallery}\n"
    ai_response += "Is there anything else I can help you with?"

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
if name == "main": app.run()