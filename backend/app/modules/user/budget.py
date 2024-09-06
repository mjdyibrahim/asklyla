@app.route("/budget", methods=["POST"]) 

def create_budget(): 
    name = request.form.get("name") 
    accommodation_budget = request.form.get("accommodation_budget") 
    food_budget = request.form.get("food_budget") 
    activity_budget = request.form.get("activity_budget") 
    transportation_budget = request.form.get("transportation_budget")

budget_info = {
    "name": name,
    "accommodation_budget": accommodation_budget,
    "food_budget": food_budget,
    "activity_budget": activity_budget,
    "transportation_budget": transportation_budget
}
return render_template("budget.html", budget=budget_info)


@app.route("/budget", methods=["POST"])
def handle_budget():
    # Code to handle budget-related requests
#Modify the user_info dictionary to include a new key called budget that will hold the estimated expenses for the trip and the actual expenses:

user_info = {
    "name": name,
    "contact_info": email,
    "travel_dates": {"from": travel_from, "to": travel_to},
    "preferences": {"accommodation_type": accommodation_type, "food_type": food_type, "activity_type": activity_type, "transportation_type": transportation_type},
    "itinerary": [],
    "budget": {"estimated": {}, "actual": {}}
}
#In the /budget route, check if the request contains a budget parameter. If it does, update the user_info dictionary with the new budget information:

@app.route("/budget", methods=["POST"])
def handle_budget():
    budget = request.json.get("budget")
    if budget:
        user_info["budget"]["estimated"] = budget
        # Code to save the new budget information to the database
# Add a new route to display the estimated and actual expenses for the trip. For example:

@app.route("/budget", methods=["GET"])
def show_budget():
    # Code to retrieve the budget information from the database
    return render_template("budget.html", estimated_budget=estimated_budget, actual_budget=actual_budget)
# Modify the chatbot responses to include information about the user's budget. For example:

# Code for responding to user's non-flight related prompt
ai_response = f"Ok, {user_info['name']}, based on your preferences and itinerary, I estimate that your trip will cost around ${user_info['budget']['estimated']} in total. Don't worry, we'll keep track of your expenses and help you stay within your budget."
# Modify the chatbot responses to ask the user for updates on their actual expenses and update the user_info dictionary with the new information. For example:

# Retrieve the most recent previous response or set it to none
if len(previous_responses) == 0:
    # Code to initialize the chatbot conversation
else:
    previous_response = previous_responses[-1]
    user_response = request.json['message']
    if "update" in user_response.lower():
        # Code to ask the user for updates on their actual expenses and update the user_info dictionary
        ai_response = "Sure, please tell me your latest expenses and I'll update your budget."
    else:
        # Code to generate a response based on the user's input
        ai_response = ...
# Add code to save the new budget information to the database whenever it is updated by the user.

@app.route("/budget", methods=["POST"])
def handle_budget():
    budget = request.json.get("budget")
    if budget:
        user_info["budget"]["actual"] = budget
        # Code to save the new budget information to the database
# Add code to retrieve the budget information from the database whenever the user accesses the /budget page.

@app.route("/budget", methods=["GET"])
def show_budget():
    # Code to retrieve the budget information from the database
    estimated_budget = db.get_estimated_budget(user_info["name"])
    actual_budget = db.get_actual_budget(user_info["name"])
    return render_template("budget.html", estimated_budget=estimated_budget, actual_budget=actual_budget)