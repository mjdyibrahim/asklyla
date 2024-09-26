from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")  # Ensure your API key is set in the environment

def get_events(location: str, interests: list):
    url = "https://www.eventbriteapi.com/v3/events/search/"
    params = {
        "location.address": location,
        "location.within": "10mi",  # can be adjusted based on the user's preference
        "categories": ",".join(interests),
    }
    headers = {
        "Authorization": f"Bearer {EVENTBRITE_API_KEY}",
    }
    response = requests.get(url, params=params, headers=headers)

    if response.ok:
        events = response.json()["events"]
        return events
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching events")

@router.post("/cultural-events")
async def fetch_cultural_events(location: str, interests: list):
    try:
        events = get_events(location, interests)
        cultural_events = [event for event in events if event.get("category") == "cultural"]
        
        if not cultural_events:
            return {"message": "No cultural events found for the given interests and location."}
        
        return {"cultural_events": cultural_events}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))