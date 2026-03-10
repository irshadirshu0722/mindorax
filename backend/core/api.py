from ninja import NinjaAPI
from apps.users.controller import router as user_router
from apps.subjects.controller import router as subject_router
from ninja.errors import HttpError, ValidationError
from django.http import Http404

api = NinjaAPI(
    title="AI Study Planner API",
    version="1.0.0"
)

api.add_router('/auth',user_router)
api.add_router('/subject',subject_router)

@api.exception_handler(HttpError)
def handle_http_error(request, exc):
    return api.create_response(request, {"message": exc.message}, status=exc.status_code)
@api.exception_handler(ValidationError)
def handle_validation_error(request, exc):
    return api.create_response(
        request,
        {"message": "Validation error", "errors": exc.errors},
        status=422,
    )

@api.exception_handler(Http404)
def handle_404(request, exc):
    return api.create_response(request, {"message": "Not found"}, status=404)

@api.exception_handler(Exception)
def handle_unexpected_error(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=500)