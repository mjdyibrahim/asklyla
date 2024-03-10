from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from gtts import gTTS
import openai
import os
import tempfile
import base64

app = Flask(__name__)

openai.api_key = "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"

# List to store previous responses
previous_responses = []

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# Bot response route
@app.route("/", methods=["POST"])
def get_bot_response():
    # Retrieve user input
    name = request.form.get("name")
    email = request.form.get("email")
    travel_from = request.form.get("travel_from")
    travel_to = request.form.get("travel_to")
    accommodation_type = request.form.get("accommodation_type")
    food_type = request.form.get("food_type")
    activity_type = request.form.get("activity_type")
    transportation_type = request.form.get("transportation_type")

    # Create user_info dictionary
    user_info = {
        "name": name,
        "email": email,
        "travel_dates": {"from": travel_from, "to": travel_to},
        "preferences": {
            "accommodation_type": accommodation_type,
            "food_type": food_type,
            "activity_type": activity_type,
            "transportation_type": transportation_type
        },
        "itinerary": []
    }

    # Use OpenAI to generate a response
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

    # Store previous response and return JSON
    previous_responses.append(previous_response)

    # Convert the text response to voice
    tts = gTTS(ai_response, lang='en')
    with tempfile.NamedTemporaryFile() as fp:
            tts.save(fp.name)
            with open(fp.name, "rb") as audio_file:
                encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
    return jsonify({"message": ai_response, "voice": encoded_string})


# Run the app
if __name__ == "__main__":
   app.run(debug=True)