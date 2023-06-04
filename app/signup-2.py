from flask import Flask, render_template, request, jsonify, session, redirect 
from dotenv import load_dotenv 
import openai 
import os

app = Flask(name) app.secret_key = os.environ.get("SECRET_KEY", "my-secret-key")

openai.api_key = "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"

List to store previous responses
previous_responses = []

@app.route("/") 
def home(): 
    return render_template("index.html")

@app.route("/", methods=["POST"]) 
def get_bot_response(): 
    if request.form.get("register"): # Process user registration 
        name = request.form.get("name") 
        email = request.form.get("email") 
        password = request.form.get("password")

    # TODO: Add code to validate user input and create a new user account
    # using a database or some other form of persistent storage

    # Redirect the user to the login page after successful registration
    return redirect("/login")

elif request.form.get("login"):
    # Process user login
    email = request.form.get("email")
    password = request.form.get("password")

    # TODO: Add code to validate user input and authenticate the user
    # using a database or some other form of persistent storage

    # Save the user's email in the session
    session["email"] = email

elif request.form.get("logout"):
    # Process user logout
    session.pop("email", None)

# Check if the user is logged in
if "email" in session:
    # User is logged in, retrieve their information from the database
    user_info = {"name": "John Doe", "email": session["email"]}
else:
    # User is not logged in, show a prompt to ask them to register or login
    user_info = None

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
    "preferences": {
        "accommodation_type": accommodation_type,
        "food_type": food_type,
        "activity_type": activity_type,
        "transportation_type": transportation_type
    },
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

    previous_response = {"user": user_response, "assistant": ai_response}
    previous_responses.append(previous_response)

return jsonify({"message": ai_response})
@app.route("/login") 
def login(): 
    return render_template("login.html")

@app.route("/register") 
def register(): 
    return render_template("register.html")

if name == "main": app.run()
