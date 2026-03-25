# Frontend Integration Guide

This guide is for frontend teams integrating with the current backend exactly as it exists today.

## Base URL

- local development: `http://localhost:8000`
- API prefix: `/api`

Examples:

- `http://localhost:8000/api/docs`
- `http://localhost:8000/api/subject/create`

## Authentication Model

The current backend behaves like a cookie-authenticated API, but login does not set the cookies for you.

### What login returns

`POST /api/auth/google-login` returns:

```json
{
  "access_token": "jwt-access-token",
  "refresh_token": "jwt-refresh-token"
}
```

### What protected routes expect

Protected routes read:

- `access_token` from cookies

Refresh reads:

- `refresh_token` from cookies

## Recommended Frontend Strategy

### Best option for Next.js or server-capable frontends

Handle Google login in a backend-for-frontend or server action, then store the returned tokens as cookies named:

- `access_token`
- `refresh_token`

After that, send requests with `credentials: "include"`.

### SPA fallback

If you are building a pure SPA, you can set cookies client-side after login. This works with the current backend, but it is less secure than server-set `HttpOnly` cookies.

## Fetch Wrapper

```ts
const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api";

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);

  if (!(init.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `API request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}
```

## Async Resource Handling

Several routes enqueue background work and require polling.

### Subject analysis flow

1. Create a subject.
2. Upload at least one file.
3. Call `POST /api/subject/analyse/{subject_id}`.
4. Poll `GET /api/subject/get/{subject_id}` until `subject_analyze` is no longer `null`.

Important:

- `SubjectResponse` does not include `is_analyzing` or `is_failed_analyze`.
- use presence of `subject_analyze` as the main completion signal

### Study plan flow

1. Call `POST /api/planning/create/{subject_id}`.
2. Poll `GET /api/planning/all/{subject_id}`.
3. Use `is_creating` and `is_failed` on the returned plan objects.

### Quiz generation flow

1. Call `POST /api/quiz/{subject_id}`.
2. Poll `GET /api/quiz/all/{subject_id}` or `GET /api/quiz/attempt/{quiz_id}`.
3. Prefer `questions.length === total_questions` as the readiness check.

Important:

- current `is_creating` and `is_failed` flags on quizzes are not fully reliable

### Quiz AI report flow

Treat `POST /api/quiz/report/{quiz_id}` as experimental until the backend task is corrected.

## File Upload Contract

Use `multipart/form-data` for:

- `POST /api/subject/file/create/{subject_id}`

Expected fields:

- `title`
- `description`
- `file`

Do not manually set `Content-Type` when sending `FormData`.

## Frontend Data Modeling Tips

- `topics`, `subtopics`, `concepts`, `key_points`, and related AI fields come back from JSON fields. Treat them as structured data.
- `SubjectResponse` does not expose a primary key, so preserve subject IDs from route params or list endpoints if you add one later.
- `StudyPlanSessionResponse.duration` is calculated in minutes by the backend.
- quiz submit requires every quiz question to be answered once.

## Error Handling Notes

Current error payloads are not fully standardized. You may encounter:

- Django Ninja validation responses
- `{"message": "..."}`
- `{"error": "..."}`

Frontend clients should be defensive when parsing error shapes.
