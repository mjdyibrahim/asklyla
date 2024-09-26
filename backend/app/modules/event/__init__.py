from app.modules.event.outdoor_activities import router as outdoor_activities_router
from app.modules.event.bear import router as bear_router
from app.modules.event.cultural_experiences import router as cultural_experiences_router
from app.modules.event.sports import router as sports_router
from app.modules.event.rsvp import router as rsvp_router
from app.modules.event.music_entertainment import router as music_entertainment_router
from app.modules.event.live_music import router as live_music_router
from app.modules.event.connect import router as connect_router
from app.modules.event.arts_crafts import router as arts_crafts_router

# List of routers for easy inclusion
routers = [
    outdoor_activities_router,
    bear_router,
    cultural_experiences_router,
    sports_router,
    rsvp_router,
    music_entertainment_router,
    live_music_router,
    connect_router,
    arts_crafts_router
]