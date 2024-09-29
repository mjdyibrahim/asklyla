from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# API key for Bandsintown
BANDSINTOWN_API_KEY = os.getenv("BANDSINTOWN_API_KEY")  # Ensure your API key is set in the environment

def get_local_events(location: str, music_preference: str):
    url = f"https://rest.bandsintown.com/v4/events?location={location}&genre={music_preference}&radius=50&per_page=3&app_id={BANDSINTOWN_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching local music events.")

    events = response.json()
    return events

@router.post("/music-events")
async def fetch_music_events(location: str, music_preference: str):
    try:
        local_events = get_local_events(location, music_preference)

        if not local_events:
            return {"message": "No local music events found for the given preferences and location."}

        # Construct a response with the local music event suggestions
        events_list = []
        for event in local_events:
            events_list.append({
                "name": event.get("title", "Unknown Event"),
                "venue": event.get("venue", {}).get("name", "Unknown Venue"),
                "city": event.get("venue", {}).get("city", "Unknown City"),
                "date": event.get("datetime", "Unknown Date"),
                "url": event.get("url", "No URL available")
            })

        return {"music_events": events_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))