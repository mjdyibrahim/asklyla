from app.modules.activity.outdoor_activities import router as outdoor_activities_router
from app.modules.activity.nature_walks import router as nature_walks_router
from app.modules.activity.adventure_activities import router as adventure_activities_router

# You can also create a list of routers if needed
routers = [
    outdoor_activities_router,
    nature_walks_router,
    adventure_activities_router
]
