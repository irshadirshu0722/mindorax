from ninja import NinjaAPI
from apps.users.controller import router
api = NinjaAPI(
    title="AI Study Planner API",
    version="1.0.0"
)

api.add_router('/auth/',router)