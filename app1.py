from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import replicate
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

# Replicate Credentials
replicate_api = os.environ.get("REPLICATE_API_TOKEN")

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


    # Initialize conversation history list in session if not present
    if "conversation" not in session:
        session["conversation"] = []

    # Add user input to conversation history
    session["conversation"].append({"role": "user", "content": user_response})

    # Get conversation history
    conversation = session["conversation"]

    if len(conversation) == 0:
        user_response = request.json['message']
        response = get_ai_response(user_response)

        ai_response = response.choices[0].message["content"].strip()

    else:
        previous_response = conversation[-1]
        user_response = request.json['message']

        response = get_ai_response(user_response)
    
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