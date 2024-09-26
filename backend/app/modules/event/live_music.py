from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# API key for Bandsintown
BANDSINTOWN_APP_ID = os.getenv("BANDSINTOWN_APP_ID")  # Ensure your API key is set in the environment

def get_live_music_events(music_preferences: str, location: str):
    url = f"https://rest.bandsintown.com/v4/events?per_page=10&sort=date&location={location}&radius=25&only_recs=true&recommendations_based_on={music_preferences}&app_id={BANDSINTOWN_APP_ID}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching live music events")

@router.post("/live-music")
async def fetch_live_music(music_preferences: str, location: str):
    try:
        live_music_events = get_live_music_events(music_preferences, location)

        if not live_music_events:
            return {"message": "No live music events found for the given preferences and location."}

        # Construct a response with the live music event suggestions
        events_list = []
        for event in live_music_events:
            events_list.append({
                "title": event.get("title", "Unknown Event"),
                "datetime": event.get("datetime", "Unknown Date"),
                "venue": event.get("venue", {}).get("name", "Unknown Venue"),
            })

        return {"live_music_events": events_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))