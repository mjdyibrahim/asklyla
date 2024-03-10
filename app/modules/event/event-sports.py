import requests

#Function to get local adventure sports experiences
def get_local_adventure_sports(user_info): # Get user's preferences 
    activity_type = user_info["preferences"]["activity_type"] 
    transportation_type = user_info["preferences"]["transportation_type"] 
    travel_to = user_info["travel_dates"]["to"] 
    location = user_info["travel_to"]

# Make API request to get local adventure sports experiences
response = requests.get(f"https://api.adventuresports.com/activities?activity_type={activity_type}&transportation_type={transportation_type}&travel_to={travel_to}&location={location}")
data = response.json()

# Extract relevant information and format it
activities = []
for activity in data["activities"]:
    activities.append({
        "name": activity["name"],
        "description": activity["description"],
        "price": activity["price"],
        "location": activity["location"]
    })

# Return the formatted activities
return activities

#Update the get_bot_response function to include local adventure sports suggestions

@app.route("/", methods=["POST"]) 
def get_bot_response(): # Get user's information 
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
    "contact_info": email,
    "travel_dates": {"from": travel_from, "to": travel_to},
    "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
    "itinerary": []
}

# Get local adventure sports suggestions
adventure_sports = get_local_adventure_sports(user_info)

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
    
    # Check if user is interested in adventure sports
    if "adventure sports" in user_response.lower():
        ai_response = "Sure, I can suggest some local adventure sports experiences for you! Here are a few options:"
        for activity in adventure_sports:
            ai_response += f"\n\nName: {activity['name']}\nDescription: {activity['description']}\nPrice: {activity['price']}\nLocation: {activity['location']}"
    else:
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