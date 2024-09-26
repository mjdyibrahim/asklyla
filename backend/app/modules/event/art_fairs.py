from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

ARTFAIR_API_KEY = os.getenv("ARTFAIR_API_KEY")  # Ensure your API key is set in the environment

@router.post("/art-fairs")
async def get_art_fairs(interests: str, location: str):
    # Make request to ArtFairCalendar API
    url = f"https://www.artfaircalendar.com/api?key={ARTFAIR_API_KEY}&interests={interests}&location={location}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Extract list of recommended art fairs from API response
        recommended_fairs = []
        for fair in data.get("fairs", []):
            recommended_fairs.append({
                "name": fair["name"],
                "date": fair["date"],
                "location": fair["location"],
                # Add more fields as desired
            })

        return {"recommended_fairs": recommended_fairs}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="No art fairs found for the given interests and location.")
