# Authentication

## Current Implementation

The backend uses Google identity verification plus JWTs.

Flow today:

1. Frontend obtains a Google `id_token`.
2. Frontend sends that token to `POST /api/auth/google-login`.
3. Backend verifies the Google token.
4. Backend creates or finds a user.
5. Backend returns `access_token` and `refresh_token` in the JSON response body.
6. Later authenticated requests rely on an `access_token` cookie.

## Important Contract Detail

There is currently a split between login and request authentication:

- login returns tokens in JSON
- middleware authenticates from cookies

This means your frontend must write the cookies after login if you want protected routes to work.

## Login Request

`POST /api/auth/google-login`

Request body:

```json
{
  "id_token": "google-id-token"
}
```

Success response:

```json
{
  "access_token": "jwt-access-token",
  "refresh_token": "jwt-refresh-token"
}
```

## Refresh Request

`GET /api/auth/refresh`

Required cookie:

- `refresh_token`

Success response:

```json
{
  "access_token": "new-jwt-access-token"
}
```

Failure response when cookie is missing:

```json
{
  "error": "Refresh token missing"
}
```

## Protected Routes

Protected routers use the custom `IsAuthenticated` class, but the real auth source is the JWT middleware.

Required cookie:

- `access_token`

## Security Notes

- The intended architecture is cookie-based.
- The current implementation does not set `HttpOnly`, `Secure`, or `SameSite` cookie flags because cookies are not written by the backend yet.
- Before production, the login and refresh flows should be converted to server-set secure cookies.
