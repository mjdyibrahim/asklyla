# Fetch Activity -> Adventure / Adrenaline.com
def get_activity_adventure(location, activity_type):
    url = "https://api.adrenaline.com/v1/activities/search"
    headers = {
        "Authorization": f"Bearer {ADRENALINE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "location": location,
        "activity_type": activity_type
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        activities = response.json()["data"]
        return activities
    else:
        return []

# Fetch Activity -> Hiking
def get_activity_hiking(user_info, location, activity_type)    # Get location coordinates from user preferences
    location = f"{travel_to}, {travel_from}"
    location_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={google_maps_api_key}"
    location_response = requests.get(location_url)
    location_data = location_response.json()
    lat = location_data["results"][0]["geometry"]["location"]["lat"]
    lng = location_data["results"][0]["geometry"]["location"]["lng"]
    
    # Query AllTrails API for hiking trails based on user preferences and location
    alltrails_url = f"https://www.alltrails.com/api/2/search?lat={lat}&lon={lng}&maxDistance=50&sort=recommended&key={alltrails_api_key}"
    alltrails_response = requests.get(alltrails_url)
    alltrails_data = alltrails_response.json()
    hiking_trails = []
    for trail in alltrails_data["data"]:
        if "family friendly" in trail["features"] and "hiking" in trail["activities"]:
            hiking_trails.append(trail)
    
    # Return the top 3 hiking trails
    if len(hiking_trails) > 0:
        ai_response = f"Here are the top {min(len(hiking_trails), 3)} hiking trails near {location}:"
        for i in range(min(len(hiking_trails), 3)):
            ai_response += f"\n{i+1}. {hiking_trails[i]['name']} ({hiking_trails[i]['length']} miles)"
    else:
        return []

# Fetch Activity -> Horsriding
def get_activity_horseriding(location, user_info)
    # make a request to HorseTrip API to get recommended horseback riding trails and lessons
        response = requests.get(HORSETRIP_API_ENDPOINT + f"/horseback_riding?location={location}&preference={horseback_riding}&key={HORSETRIP_API_KEY}")
        if response.status_code == 200:
            trails = response.json()["trails"]
            user_info["horseback_riding_trails"] = trails # add recommended horseback riding trails and lessons to user_info
        else:
            print(f"Error fetching horseback riding trails: {response.status_code}")

# Fetch Activity -> ebird.org
def get_actvitiy_birdwatching(user_info): # Get user's location location = user_info['travel_from']

    # Make request to eBird API
    response = requests.get(f'https://api.ebird.org/v2/ref/hotspot/geo?lat={location["lat"]}&lng={location["lng"]}&dist=10')

    # Parse response and filter results
    results = response.json()
    bird_species = user_info['preferences']['bird_species']
    habitat_type = user_info['preferences']['habitat_type']
    recommendations = []
    for result in results:
        if bird_species in result['species'] and habitat_type in result['habitat']:
            recommendations.append(result['name'])

    return recommendations

# Fetch Activity -> Volunteer
def get_activity_volunteer(): 
    user_info = request.json['user_info'] 
    location = user_info['location'] 
    interests = user_info['interests']

    # Make a request to the VolunteerMatch API
    response = requests.get(f"https://www.volunteermatch.org/search/index.jsp?l={location}&k={interests}&submitsearch=Search")

    # Parse the response to get the volunteer opportunities
    # Add code to parse the response and extract the volunteer opportunities

    # Return the volunteer opportunities to the user
    # Add code to return the volunteer opportunities to the user

    # Fetch Experiences -> Cultural

def get_experience_cultural(user_info): # Extract user's location from travel_from 
    location = user_info["travel_dates"]["from"]

    # Extract user's interests
    interests = user_info["preferences"]["activity_type"]

    # Make API call to fetch cultural experiences in user's location
    response = requests.get("https://api.yelp.com/v3/businesses/search", 
                        headers={"Authorization": "Bearer API_KEY_HERE"}, 
                        params={"location": location, "categories": "museums, art galleries"})

    # Filter results based on user's interests
    results = []
    for business in response.json()["businesses"]:
        if any(interest.lower() in business["categories"] for interest in interests):
             results.append({"name": business["name"], "address": business["location"]["address1"], "phone": business["phone"]})

    return results

def get_experience_sightseeing()

def get_experience_beach()

# Fetch Venues -> Spa

"""
Install the SpaFinder API package using pip:
!pip install spafinder
Import the required modules in the code:
from spafinder import SpaFinderClient
from spafinder.exceptions import SpaFinderException
Add a new function to get spa recommendations based on the user's preferences and location:

    # Check if the user requests spa recommendations
    if 'spa' in user_response.lower():
        # Get spa recommendations based on user's preferences and location
        spa_recommendation = get_spa_recommendation(user_info)
        
        # Return the spa recommendations to the user
        return jsonify({"message": spa_recommendation})
    
    else:

"""
def get_venue_spa(user_info):
    """Get spa recommendations based on user's preferences and location"""
    
    # Get user's preferences and location
    preferences = user_info['preferences']
    location = user_info['travel_to']
    
    # Initialize SpaFinder client
    client = SpaFinderClient(api_key='your_api_key_here')
    
    try:
        # Search for spas based on user's preferences and location
        results = client.search(location=location, **preferences)
        
        # Get the top 3 spa recommendations
        top_results = results[:3]
        
        # Format the recommendations as a string
        recommendations = '\n'.join([f'{r.name} in {r.city}, {r.state}' for r in top_results])
        
        # Return the recommendations
        return f"Here are some spas you might like:\n{recommendations}"
    
    except SpaFinderException:
        # Return an error message if there's an issue with the API
        return "Sorry, I couldn't find any spas that match your preferences."

def get_venue_yogastudio():
    return []

def get_venue_cafe():
    return []

def get_venue_restaurant():
    return []

def get_venue_bar():
    return []

def get_venue_museum():
    return []

def get_venue_

# Check if user wants yoga recommendations
def get_venue_yoga(user_info):
    # Get yoga recommendations using Mindbody API
    response = requests.get(f"https://api.mindbodyonline.com/public/v6/staff/staff?categoryIds={yoga_type}&location={location}&limit=10", headers={"Api-Key": os.getenv("MINDBODY_API_KEY")})
    studios = response.json()["Studios"]
    recommendations = []
    for studio in studios:
        recommendations.append({"name": studio["Name"], 
                                "address": studio["Address"]["AddressLine1"], 
                                "city": studio["Address"]["City"], 
                                "state": studio["Address"]["StateProvince"], 
                                "zip": studio["Address"]["PostalCode"], 
                                "phone": studio["Phone"]})
        

def get_event_artfaor():
    return []


def get_theater_performances(location, interests):
    url = f"https://api.todaytix.com/x/2.0/performances?city={location}&interests={interests}&apikey={TODAYTIX_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        performances = response.json()["response"]["results"]
        return performances
    else:
        return None
