from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/suggest")
async def get_adventure_activities(location: str, activity_type: str):
    # Placeholder for the actual implementation
    # This function should make a request to the Adrenaline API
    if activity_type == "adventure":
        activities = [
            {"name": "Skydiving", "location": location},
            {"name": "Bungee Jumping", "location": location}
        ]
        return activities
    else:
        raise HTTPException(status_code=400, detail="Invalid activity type")
