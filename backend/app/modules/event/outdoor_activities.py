from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

router = APIRouter()

# Load environment variables
load_dotenv()

# AllTrails API key
alltrails_key = os.getenv("ALLTRAILS_API_KEY")

@router.post("/outdoor-activities")
async def get_outdoor_activities(location: dict, activity_type: str):
    if activity_type.lower() != "outdoor":
        raise HTTPException(status_code=400, detail="Activity type must be 'Outdoor' to fetch trail recommendations.")

    # Get nearby trails from AllTrails API
    url = f"https://www.alltrails.com/api/2/search/?key={alltrails_key}&q=hiking&lat={location['lat']}&lon={location['lng']}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching trails from AllTrails API.")

    trails = response.json().get("places", [])
    
    # Get top 3 trails based on user's preference
    top_trails = []
    for trail in trails:
        if trail.get("activity_type_name") == activity_type and trail.get("rating", 0) >= 4:
            top_trails.append(trail)
        if len(top_trails) == 3:
            break

    if not top_trails:
        return {"message": "No suitable trails found for the specified location."}

    # Create a response message with trail recommendations
    response_message = []
    for trail in top_trails:
        response_message.append({
            "name": trail['name'],
            "city": trail['city'],
            "state": trail['state'],
        })

    return {"trails": response_message}