
@app.route("/itinerary", methods=["POST"]) 
def save_itinerary(): 
    itinerary = request.json['itinerary'] # Save the itinerary to a database or file for future retrieval 
    return jsonify({"message": "Itinerary saved successfully!"})

@app.route("/itinerary", methods=["GET"]) 
def view_itinerary(): # Retrieve the saved itinerary from the database or file 
    itinerary = get_saved_itinerary() 
    return render_template("itinerary.html", itinerary=itinerary)

# In the save_itinerary() function, you can retrieve the itinerary data from the request and save it to a database or file for future retrieval. You can then return a JSON response indicating that the itinerary was saved successfully.

# In the view_itinerary() function, you can retrieve the saved itinerary from the database or file and pass it to a new HTML template called "itinerary.html". This template can display the itinerary information in a user-friendly way, such as a table or list.


#Create a new route for saving the itinerary:
@app.route("/save-itinerary", methods=["POST"])
def save_itinerary():
    user_info = request.json
    # Code to save the itinerary to a database or file
    return jsonify({"message": "Itinerary saved successfully!"})
# Add a button or link in the HTML template for users to save their itinerary:
<form id="itinerary-form">
  <!-- HTML code for the itinerary form fields -->
  <button type="submit" class="btn btn-primary">Save Itinerary</button>
</form>
Add JavaScript code to handle the form submission and send the itinerary data to the server:
$(document).ready(function() {
  $("#itinerary-form").submit(function(event) {
    event.preventDefault();
    var formData = $(this).serializeArray();
    $.ajax({
      url: "/save-itinerary",
      type: "POST",
      data: JSON.stringify(formData),
      contentType: "application/json",
      success: function(response) {
        alert(response.message);
      },
      error: function(xhr, status, error) {
        console.log(xhr.responseText);
      }
    });
  });
});
# Create a new route for viewing the saved itinerary:
@app.route("/view-itinerary")
def view_itinerary():
    # Code to retrieve the saved itinerary from the database or file
    user_info = {}  # Replace this with the actual itinerary data
    return render_template("itinerary.html", user_info=user_info)
# Create a new HTML template for displaying the itinerary:
{% extends "base.html" %}

{% block content %}
  <h2>My Itinerary</h2>
  <ul>
    {% for activity in user_info.itinerary %}
      <li>{{ activity }}</li>
    {% endfor %}
  </ul>
{% endblock %}
# Add a link or button in the HTML template for users to view their saved itinerary:
<a href="/view-itinerary" class="btn btn-primary">View Itinerary</a>
# With these changes, users will be able to save their itinerary by submitting the form, and view it later by clicking the link or button. You will need to modify the code to use a database or file to store the itinerary data, depending on your requirements.

