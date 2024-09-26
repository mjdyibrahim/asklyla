from fastapi import APIRouter, HTTPException
from alltrails import Client
from geopy.geocoders import Nominatim

router = APIRouter()

@router.post("/suggested_trails")
async def suggested_trails(fitness_level: str, location: str):
    geolocator = Nominatim(user_agent="my_app")
    location_data = geolocator.geocode(location)
    
    if not location_data:
        raise HTTPException(status_code=400, detail="Location not found")

    latitude, longitude = location_data.latitude, location_data.longitude
    client = Client(api_key="your_api_key_here")
    trails = client.get_trails_by_coordinates(latitude, longitude, max_distance=10, max_results=10, min_difficulty=fitness_level)

    response = [{"name": trail.name, "location": trail.location, "difficulty": trail.difficulty} for trail in trails]
    return response