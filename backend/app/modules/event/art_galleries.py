from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# API key for art gallery recommendations
art_api_key = os.getenv("ART_API_KEY")  # Ensure your API key is set in the environment

@router.post("/art-galleries")
async def get_art_galleries(location: str, interest: str):
    if interest.lower() != "art":
        raise HTTPException(status_code=400, detail="Interest must be 'art' to fetch gallery recommendations.")

    # Get art gallery recommendations based on user's location using third-party API
    art_response = requests.get(f"https://api.art.com/art-gallery/v1/galleries?apiKey={art_api_key}&location={location}&pageNum=1&pageSize=5")

    if art_response.status_code != 200:
        raise HTTPException(status_code=art_response.status_code, detail="Error fetching art galleries.")

    galleries = art_response.json().get("galleries", [])
    if not galleries:
        return {"message": "No art galleries found for the specified location."}

    gallery_names = [gallery["galleryName"] for gallery in galleries]

    # Build response with gallery recommendations
    ai_response = f"Here are some art galleries in {location} you might be interested in:\n"
    for gallery in gallery_names:
        ai_response += f"- {gallery}\n"
    ai_response += "Is there anything else I can help you with?"

    return {"message": ai_response}