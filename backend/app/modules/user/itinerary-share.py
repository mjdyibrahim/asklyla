
@app.route("/itinerary", methods=["POST"]) 

def save_itinerary(): 
    name = request.form.get("name") 
    email = request.form.get("email") 
    itinerary = request.form.get("itinerary") 
    categories = request.form.get("categories")

# Save the itinerary information to the database
# ...

# Send the itinerary to the user and any recipients they specified
# ...

return jsonify({"message": "Itinerary saved and sent to specified recipients."})