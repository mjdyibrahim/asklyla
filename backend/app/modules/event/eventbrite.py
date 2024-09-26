from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")  # Ensure your API key is set in the environment

@router.post("/suggestions")
async def get_suggestions(interests: str, location: str):
    # Make API call to retrieve relevant events
    url = "https://api.eventbrite.com/v3/events/search/"
    params = {
        "q": interests,
        "location.address": location,
        "sort_by": "date",
        "token": EVENTBRITE_API_KEY  # Include the API key in the request
    }
    
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching event suggestions")

    events = response.json().get("events", [])

    # Prepare suggestions for the user
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

    return {"suggestions": suggestions}