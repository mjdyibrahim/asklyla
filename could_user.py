# Check if user is logged in
if "username" in session:
    username = session["username"]
    # Retrieve user's preferences and itinerary from database
    user_info = mongo.db.users.find_one({"username": username})
    if user_info:
        user_info["_id"] = str(user_info["_id"])
    else:
        user_info = {}

#if 'flight' in user_response:
    #flight_recommendation = get_flight_recommendation(user_info)
    # Add code to display the flight recommendation to the user
#else:
    # Code for responding to user's non-flight related prompt
