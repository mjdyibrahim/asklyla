
@app.route("/itineraries", methods=["POST"])
def create_itinerary():
    itinerary_name = request.form.get("itinerary_name")
    itinerary = request.form.get("itinerary")
    # Save the itinerary to the user's account
    # You can use a database or a file system to store the itinerary data
    # Make sure to associate the itinerary with the user's account
    return jsonify({"message": "Itinerary created successfully!"})
In this code snippet, you're creating a new route called /itineraries that will handle the itinerary creation and saving process. When a user submits a new itinerary, you'll retrieve the itinerary name and itinerary data from the request form data, and then save it to the user's account.

To allow users to switch between their saved itineraries, you can add a new route that will retrieve all the saved itineraries for the user's account:

@app.route("/itineraries", methods=["GET"])
def get_itineraries():
    # Retrieve all the saved itineraries for the user's account
    # You can use a database or a file system to retrieve the itinerary data
    # Make sure to associate the itineraries with the user's account
    itineraries = []
    return jsonify({"itineraries": itineraries})
In this code snippet, you're creating a new route called /itineraries that will retrieve all the saved itineraries for the user's account. You'll retrieve the itinerary data from the database or file system, and then return it as a JSON response.

To switch between the saved itineraries, you can add a new parameter to the / route that will allow the user to specify which itinerary they want to use:

@app.route("/", methods=["POST"])
def get_bot_response():
    itinerary_name = request.form.get("itinerary_name")
    # Retrieve the selected itinerary from the user's account
    # You can use a database or a file system to retrieve the itinerary data
    # Make sure to associate the itinerary with the user's account
    itinerary = {}
    # Use the selected itinerary to generate a response
    return jsonify({"message": ai_response})
In this code snippet, you're adding a new parameter to the / route called itinerary_name. When the user submits a new message, you'll retrieve the selected itinerary from the user's account, and then use it to generate a response.
