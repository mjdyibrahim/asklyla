from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# API key for food-related activities
food_api_key = os.getenv("FOOD_API_KEY")  # Ensure your API key is set in the environment

@router.post("/food-markets")
async def get_food_markets(location: str, food_type: str):
    if 'food' not in food_type:
        raise HTTPException(status_code=400, detail="Food type must be specified.")

    # Get user location using IP address
    ip_address = "user_ip_address"  # Replace with actual user IP retrieval logic if needed
    location_url = f"http://ip-api.com/json/{ip_address}"
    location_response = requests.get(location_url).json()
    latitude = location_response['lat']
    longitude = location_response['lon']

    # Use food API to get nearby food markets and experiences
    food_url = f"https://api.yelp.com/v3/businesses/search?latitude={latitude}&longitude={longitude}&categories=food&sort_by=rating&limit=3"
    headers = {
        "Authorization": f"Bearer {food_api_key}",
        "Content-Type": "application/json"
    }
    food_response = requests.get(food_url, headers=headers).json()

    # Format response with top 3 food markets and experiences
    if 'businesses' not in food_response:
        raise HTTPException(status_code=404, detail="No food markets found.")

    food_recommendation = []
    for i, business in enumerate(food_response['businesses']):
        food_recommendation.append({
            "name": business['name'],
            "address": business['location']['address1'],
            "rating": business.get('rating', 'N/A')
        })

    return {"food_markets": food_recommendation}