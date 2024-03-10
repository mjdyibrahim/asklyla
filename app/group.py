Add a new route to handle group creation and joining:
@app.route("/groups", methods=["POST"])
def handle_groups():
    action = request.form.get("action")
    group_name = request.form.get("group_name")
    user_id = request.form.get("user_id")

    if action == "create":
        # create a new group and add the user to it
        group_id = create_group(group_name, user_id)
        return jsonify({"success": True, "message": "Group created successfully", "group_id": group_id})
    elif action == "join":
        group_id = request.form.get("group_id")
        if join_group(group_id, user_id):
            return jsonify({"success": True, "message": "Joined group successfully"})
        else:
            return jsonify({"success": False, "message": "Failed to join group"})
Implement the create_group and join_group functions:
def create_group(group_name, user_id):
    # create a new group in the database and add the user to it
    # return the group ID
    pass

def join_group(group_id, user_id):
    # add the user to the specified group in the database
    # return True if successful, False otherwise
    pass
Modify the user_info dictionary to include the user's group information:
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
    "itinerary": [],
    "group_id": group_id,  # add the group ID to the user's info
    "group_name": group_name  # add the group name to the user's info
}
Modify the chat prompts to include group-related messages: