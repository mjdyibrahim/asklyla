from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import replicate
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

# Replicate Credentials
replicate_api = os.environ.get("REPLICATE_API_TOKEN")

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


    # Initialize conversation history list in session if not present
    if "conversation" not in session:
        session["conversation"] = []

    # Add user input to conversation history
    session["conversation"].append({"role": "user", "content": user_response})

    # Get conversation history
    conversation = session["conversation"]

    if len(conversation) == 0:
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
    conversation.append(previous_response)
    session["conversation"].add_assistant_message(ai_response)

    
    return jsonify({"message": ai_response})


def get_ai_response(user_response):
    string_dialogue = """You are Lyla, a 33 Arab female Travel Assistant with the mission to help user to find their optimal travel flights, 
                            accommodations and experiences in the Arab world"""
    for dict_message in session["conversation"].messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
    ai_response = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {user_response} Assistant: ",
                                  "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    return ai_response


if __name__ == "__main__":
    app.run()
>>>>>>> origin/main
