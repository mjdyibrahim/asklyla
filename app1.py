from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai
import os

app = Flask(__name__)

openai.api_key = "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"

# List to store previous responses
previous_responses = []

<<<<<<< HEAD

=======
>>>>>>> origin/main
@app.route("/")
def home():
    return render_template("index.html")

<<<<<<< HEAD

@app.route("/", methods=["POST"])
def get_bot_response():
=======
@app.route("/", methods=["POST"])
def get_bot_response():

>>>>>>> origin/main
    name = request.form.get("name")
    email = request.form.get("email")
    travel_from = request.form.get("travel_from")
    travel_to = request.form.get("travel_to")
    accommodation_type = request.form.get("accommodation_type")
    food_type = request.form.get("food_type")
    activity_type = request.form.get("activity_type")
    transportation_type = request.form.get("transportation_type")
<<<<<<< HEAD

=======
    
>>>>>>> origin/main
    user_info = {
        "name": name,
        "contact_info": email,
        "travel_dates": {"from": travel_from, "to": travel_to},
<<<<<<< HEAD
        "preferences": {
            "accommodation_type": accommodation_type,
            "food_type": food_type,
            "activity_type": activity_type,
            "transportation_type": transportation_type,
        },
        "itinerary": [],
    }

    # if 'flight' in user_response:
    # flight_recommendation = get_flight_recommendation(user_info)
    # Add code to display the flight recommendation to the user
    # else:
    # Code for responding to user's non-flight related prompt

    # Retrieve the most recent previous response or set it to none
    if len(previous_responses) == 0:
        user_response = request.json["message"]
=======
        "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
        "itinerary": []
    }

    #if 'flight' in user_response:
    #flight_recommendation = get_flight_recommendation(user_info)
    # Add code to display the flight recommendation to the user
    #else:
    # Code for responding to user's non-flight related prompt
        
    # Retrieve the most recent previous response or set it to none
    if len(previous_responses) == 0:
        user_response = request.json['message']
>>>>>>> origin/main
        ai_response = ""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
<<<<<<< HEAD
                {
                    "role": "system",
                    "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need.",
                },
                {"role": "user", "content": ""},
                {
                    "role": "assistant",
                    "content": "Hi, I'm Lyla, your personal travel companion! Before we start, can you tell me your name?",
                },
                {"role": "user", "content": user_response},
=======
            {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need."}, 
             {"role": "user", "content": ""},           
            {"role": "assistant", "content": "Hi, I'm Lyla, your personal travel companion! Before we start, can you tell me your name?"},                  
            {"role": "user", "content": user_response}
>>>>>>> origin/main
            ],
            temperature=0.7,
            max_tokens=300,
            frequency_penalty=0,
<<<<<<< HEAD
            presence_penalty=0,
        )

=======
            presence_penalty=0
        )
    
>>>>>>> origin/main
        ai_response = response.choices[0].message["content"].strip()

    else:
        previous_response = previous_responses[-1]
<<<<<<< HEAD
        user_response = request.json["message"]
        prompt = [
            {
                "role": "system",
                "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need.",
            },
            {"role": "user", "content": previous_response["user"]},
            {"role": "assistant", "content": previous_response["assistant"]},
            {"role": "user", "content": user_response},
=======
        user_response = request.json['message']
        prompt = [
            {"role": "system", "content": "You are Lyla a 33 year old Arab female Travel Companion who helps the user form or adjust their travel itineary based on their perferences and personality, objectives and current life circumstances and help them book all the services they need."},
            {"role": "user", "content": previous_response['user']},
            {"role": "assistant", "content": previous_response['assistant']},
            {"role": "user", "content": user_response}
>>>>>>> origin/main
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.7,
            max_tokens=300,
            frequency_penalty=0,
<<<<<<< HEAD
            presence_penalty=0,
        )

        ai_response = response.choices[0].message["content"].strip()

    previous_response = {"user": user_response, "assistant": ai_response}
    previous_responses.append(previous_response)

    return jsonify({"message": ai_response})


if __name__ == "__main__":
    app.run()
=======
            presence_penalty=0
        )
    
        ai_response = response.choices[0].message["content"].strip()
        
    previous_response = {"user": user_response, "assistant": ai_response}
    previous_responses.append(previous_response)
    
    return jsonify({"message": ai_response})

if __name__ == "__main__":
    app.run()
>>>>>>> origin/main
