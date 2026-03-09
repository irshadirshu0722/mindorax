# Authentication Feature

## Overview

The system uses a modern authentication approach based on OAuth and JSON Web Tokens (JWT).

Authentication is designed to be secure, scalable, and compatible with modern frontend frameworks.

---

# Authentication Strategy

The system uses:

* Google OAuth for login
* JWT tokens for session management
* HttpOnly cookies for token storage

This approach combines the benefits of OAuth identity with stateless API authentication.

---

# Authentication Flow

Step 1 – User Login

User selects “Login with Google”.

The frontend redirects the user to the Google OAuth authorization page.

Step 2 – OAuth Verification

After successful login, Google returns an authorization code.

The backend exchanges this code for a verified user identity.

Step 3 – User Creation

If the user does not exist:

* A new user record is created
* User information is stored in the database

Step 4 – Token Generation

Two tokens are created:

Access Token

* Short-lived
* Used for API authentication

Refresh Token

* Long-lived
* Used to issue new access tokens

Step 5 – Cookie Storage

Tokens are stored in secure HttpOnly cookies.

This prevents access by client-side JavaScript and reduces XSS risk.

---

# Token Lifecycle

Access Token

* Lifetime: ~30 minutes
* Used for authenticating API requests

Refresh Token

* Lifetime: ~7 days
* Used to obtain new access tokens

---

# Authenticated Requests

For each request:

1. Browser automatically sends cookies
2. Middleware reads the access token
3. Token is verified
4. User is attached to the request context

---

# Logout Process

Logout clears authentication cookies.

The client becomes unauthenticated immediately.

---

# Security Measures

The authentication system includes several security practices:

* HttpOnly cookies
* Secure cookie flag
* SameSite protection
* Token expiration
* Server-side verification
* No tokens stored in local storage

---

# API Endpoints

Authentication endpoints include:

POST /auth/google-login
POST /auth/refresh
POST /auth/logout
GET /auth/me

---

# Future Improvements

Potential improvements include:

* Token rotation
* Token blacklist in Redis
* Multi-provider OAuth
* Device session management
