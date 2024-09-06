@app.route("/packing-list", methods=["GET"]) 
def get_packing_list(): # Retrieve the user's saved packing list from the database # Categorize the items by type # Mark completed items # Render the packing list template with the data return render_template("packing_list.html", packing_list=packing_list)

@app.route("/packing-list", methods=["POST"]) 
def save_packing_list(): # Retrieve the user's input from the form # Save the packing list to the database # Redirect the user back to the packing list page return redirect(url_for("get_packing_list"))
