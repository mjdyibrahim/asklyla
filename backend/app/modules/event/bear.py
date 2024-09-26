from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# Set your OpenAI API key if needed for other purposes
# openai.api_key = os.getenv("OPENAI_API_KEY")  # Uncomment if you need OpenAI for other functionalities

# Third-party API endpoints
BREWERY_API_URL = "https://api.openbrewerydb.org/breweries"
BEER_API_URL = "https://api.punkapi.com/v2/beers"

@router.post("/recommendations")
async def get_recommendations(location: str, interests: str):
    # Fetch recommendations from Untappd API
    url = f"https://api.untappd.com/v4/search/beer?q={interests}&limit=10&lat={location['lat']}&lng={location['lng']}&radius=10"
    response = requests.get(url, headers={"Authorization": "Bearer <YOUR_API_KEY>"})

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching recommendations")

    # Parse the response and send back the recommendations to the user
    recommendations = []
    for item in response.json()["response"]["beers"]["items"]:
        brewery = item["brewery"]["brewery_name"]
        beer = item["beer_name"]
        recommendations.append(f"{beer} from {brewery}")

    return {"recommendations": recommendations}

@router.post("/brewery-beers")
async def get_brewery_beers(location: str, brewery_type: str, beer_type: str):
    # Make API requests to get relevant information based on user's preferences and location
    brewery_response = requests.get(f"{BREWERY_API_URL}?by_city={location}&by_type={brewery_type}")
    beer_response = requests.get(f"{BEER_API_URL}?beer_name={beer_type}")

    if brewery_response.status_code != 200 or beer_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching brewery or beer information")

    # Parse the responses and extract relevant information
    breweries = [b["name"] for b in brewery_response.json()]
    beers = [b["name"] for b in beer_response.json()]

    # Generate a response to suggest local breweries and beer tastings
    response_message = []
    if breweries and beers:
        response_message.append(f"I found these local breweries that might interest you: {', '.join(breweries)}.")
        response_message.append(f"And you might want to try these beers: {', '.join(beers)}.")
    elif breweries:
        response_message.append(f"I found these local breweries that might interest you: {', '.join(breweries)}.")
    elif beers:
        response_message.append(f"You might want to try these beers: {', '.join(beers)}.")
    else:
        response_message.append("Sorry, I couldn't find any local breweries or beer tastings that match your preferences.")

    return {"message": " ".join(response_message)}
