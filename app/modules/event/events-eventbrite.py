import requests

# Get suggestions for local events and experiences
@app.route("/suggestions", methods=["POST"])
def get_suggestions():
    interests = request.form.get("interests")
    location = request.form.get("location")

    # Make API call to retrieve relevant events
    response = requests.get("https://api.eventbrite.com/v3/events/search/", params={
        "q": interests,
        "location.address": location,
        "sort_by": "date",
    })
    events = response.json()["events"]

    # Display events to the user and provide RSVP and connect options
    suggestions = []
    for event in events:
        suggestion = {
            "name": event["name"]["text"],
            "description": event["description"]["text"],
            "date": event["start"]["local"],
            "location": event["venue"]["name"],
            "rsvp_link": event["url"],
            "connect_link": event["url"],
        }
        suggestions.append(suggestion)

    return jsonify({"suggestions": suggestions})