from ninja.security import HttpBearer,django_auth
from ninja.errors import HttpError


class IsAuthenticated(HttpBearer):

    def __call__(self, request):
        # As we already run the middleware we can override this part
        return self.authenticate(request)
    def authenticate(self, request, token=None):
        print(request.user)
        if not request.user or not request.user.is_authenticated:
            raise HttpError(401, "Authentication required")
        
        return request.user