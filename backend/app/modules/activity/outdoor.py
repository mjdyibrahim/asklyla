from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.post("/suggest")
async def get_outdoor_activities(preferences: str, location: str):
    api_key = "your_api_key_here"
    url = f"https://api.example.com/outdoor_activities?preferences={preferences}&location={location}&api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        activities = response.json()
        return activities
    else:
        raise HTTPException(status_code=404, detail="Activities not found")