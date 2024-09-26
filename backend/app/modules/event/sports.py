from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# AllTrails API key
ADVENTURE_SPORTS_API_URL = "https://api.adventuresports.com/activities"

def get_local_adventure_sports(user_info):
    # Get user's preferences 
    activity_type = user_info["preferences"]["activity_type"] 
    transportation_type = user_info["preferences"]["transportation_type"] 
    travel_to = user_info["travel_dates"]["to"] 
    location = user_info["travel_to"]

    # Make API request to get local adventure sports experiences
    response = requests.get(f"{ADVENTURE_SPORTS_API_URL}?activity_type={activity_type}&transportation_type={transportation_type}&travel_to={travel_to}&location={location}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching adventure sports.")

    data = response.json()

    # Extract relevant information and format it
    activities = []
    for activity in data.get("activities", []):
        activities.append({
            "name": activity["name"],
            "description": activity["description"],
            "price": activity["price"],
            "location": activity["location"]
        })

    return activities

@router.post("/adventure-sports")
async def fetch_adventure_sports(user_info: dict):
    try:
        adventure_sports = get_local_adventure_sports(user_info)

        if not adventure_sports:
            return {"message": "No local adventure sports found for the specified preferences."}

        return {"adventure_sports": adventure_sports}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))