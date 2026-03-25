# API Reference

This reference documents the current API contract as implemented in the repository.

## Runtime API Docs

When the server is running:

- Swagger UI: `/api/docs`
- OpenAPI JSON: `/api/openapi.json`

## Base URL And Auth

- Base API prefix: `/api`
- Protected endpoints require the `access_token` cookie
- Refresh requires the `refresh_token` cookie

## Endpoint Summary

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| POST | `/api/auth/google-login` | No | Exchange Google token for JWTs |
| GET | `/api/auth/refresh` | Cookie | Refresh access token |
| POST | `/api/subject/create` | Yes | Create a subject |
| GET | `/api/subject/get/{subject_id}` | Yes | Get one subject |
| PUT | `/api/subject/update/{subject_id}` | Yes | Update one subject |
| DELETE | `/api/subject/delete/{subject_id}` | Yes | Delete one subject |
| POST | `/api/subject/file/create/{subject_id}` | Yes | Upload a file to a subject |
| PUT | `/api/subject/file/update/{file_id}` | Yes | Update subject file metadata |
| DELETE | `/api/subject/file/delete/{file_id}` | Yes | Delete a subject file |
| POST | `/api/subject/analyse/{subject_id}` | Yes | Start AI subject analysis |
| POST | `/api/planning/create/{subject_id}` | Yes | Start AI study plan generation |
| GET | `/api/planning/all/{subject_id}` | Yes | List all study plans for a subject |
| GET | `/api/planning/plan/{plan_id}` | Yes | Get one study plan |
| POST | `/api/planning/plan/complete/{plan_item_id}` | Yes | Mark a plan item as completed with a study session |
| POST | `/api/quiz/{subject_id}` | Yes | Start AI quiz generation |
| GET | `/api/quiz/all/{subject_id}` | Yes | List quizzes for a subject |
| GET | `/api/quiz/attempt/{quiz_id}` | Yes | Get quiz details and questions |
| POST | `/api/quiz/submit/{quiz_id}` | Yes | Submit quiz answers |
| POST | `/api/quiz/report/{quiz_id}` | Yes | Request AI quiz report |

## Authentication

### `POST /api/auth/google-login`

Purpose:

- verify Google identity
- create or load the user
- return JWT access and refresh tokens

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

Frontend note:

- store both tokens in cookies named `access_token` and `refresh_token`

### `GET /api/auth/refresh`

Required cookie:

- `refresh_token`

Success response:

```json
{
  "access_token": "new-jwt-access-token"
}
```

Possible failure:

```json
{
  "error": "Refresh token missing"
}
```

## Subjects

### `POST /api/subject/create`

Content type:

- `application/json`

Request body:

```json
{
  "title": "Backend System Design",
  "description": "Study API architecture and storage layers.",
  "goal": "Build a production-ready backend project.",
  "deadline": "2026-04-15",
  "status": "active"
}
```

Success response:

```json
{
  "files": [],
  "subject_analyze": null,
  "title": "Backend System Design",
  "description": "Study API architecture and storage layers.",
  "goal": "Build a production-ready backend project.",
  "deadline": "2026-04-15",
  "status": "active"
}
```

Important notes:

- the response does not include the subject `id`
- the response does not include analysis status flags

### `GET /api/subject/get/{subject_id}`

Success response shape:

```json
{
  "files": [
    {
      "full_url": "http://localhost:8000/media/subjects/networks.pdf",
      "id": 3,
      "created_at": "2026-03-25T10:30:00Z",
      "update_at": "2026-03-25T10:30:00Z",
      "subject": 12,
      "file": "/media/subjects/networks.pdf",
      "file_type": "application/pdf",
      "title": "Lecture Notes",
      "description": "Primary reference PDF"
    }
  ],
  "subject_analyze": {
    "id": 5,
    "created_at": "2026-03-25T11:00:00Z",
    "update_at": "2026-03-25T11:00:00Z",
    "subject": 12,
    "difficulty_level": "medium",
    "summary": "Core networking topics and protocols.",
    "topics": ["OSI model", "TCP/IP", "routing"],
    "subtopics": [
      {
        "topic": "OSI model",
        "subtopics": ["layers", "encapsulation"]
      }
    ],
    "concepts": [
      {
        "term": "packet",
        "definition": "a unit of network data"
      }
    ],
    "topic_wise_priority": [
      {
        "topic": "routing",
        "priority": "high"
      }
    ],
    "key_points": ["Understand layer responsibilities"],
    "recommended_focus": ["routing"],
    "estimated_hours": 18
  },
  "title": "Computer Networks",
  "description": "Semester networking module",
  "goal": "Pass the final exam",
  "deadline": "2026-05-15",
  "status": "active"
}
```

### `PUT /api/subject/update/{subject_id}`

Request body:

Same shape as subject creation.

Success response:

- same shape as `GET /api/subject/get/{subject_id}`

### `DELETE /api/subject/delete/{subject_id}`

Success response:

```json
{
  "message": "Successfully deleted the subject"
}
```

### `POST /api/subject/file/create/{subject_id}`

Content type:

- `multipart/form-data`

Form fields:

- `title`
- `description`
- `file`

Success response:

```json
{
  "full_url": "http://localhost:8000/media/subjects/networks.pdf",
  "id": 3,
  "created_at": "2026-03-25T10:30:00Z",
  "update_at": "2026-03-25T10:30:00Z",
  "subject": 12,
  "file": "/media/subjects/networks.pdf",
  "file_type": "application/pdf",
  "title": "Lecture Notes",
  "description": "Primary reference PDF"
}
```

Implementation note:

- `file_type` is populated from the uploaded MIME type in the current service

### `PUT /api/subject/file/update/{file_id}`

Content type:

- `application/json`

Request body:

```json
{
  "title": "Updated file title",
  "description": "Updated description"
}
```

Success response:

- same shape as file creation response

### `DELETE /api/subject/file/delete/{file_id}`

Success response:

```json
{
  "message": "Subject file deleted successfully"
}
```

### `POST /api/subject/analyse/{subject_id}`

Purpose:

- enqueue AI subject analysis

Success response:

```json
{
  "message": "Subject start analyzing. You are in Free Mode So It takes time please come later"
}
```

Frontend polling strategy:

- keep calling `GET /api/subject/get/{subject_id}`
- analysis is ready when `subject_analyze` becomes non-null

## Planning

### `POST /api/planning/create/{subject_id}`

Content type:

- `application/json`

Request body:

```json
{
  "topics": ["REST APIs", "database design", "background jobs"],
  "starting_date": "2026-03-26T09:00:00Z",
  "end_date": "2026-04-05T18:00:00Z",
  "description": "Prepare for the backend system design interview track."
}
```

Success response:

```json
{
  "message": "It's being created, it's take time, please come later"
}
```

Important notes:

- this endpoint does not return the created plan ID
- poll the list or detail endpoints to discover the generated plan

### `GET /api/planning/all/{subject_id}`

Success response example:

```json
[
  {
    "plan_items": [
      {
        "plan_session": null,
        "id": 9,
        "created_at": "2026-03-25T12:00:00Z",
        "update_at": "2026-03-25T12:00:00Z",
        "plan": 4,
        "topic": "REST APIs",
        "description": "Review status codes, request validation, and error handling.",
        "estimated_hours": 2,
        "starting_date_time": "2026-03-27T09:00:00Z",
        "end_date_time": "2026-03-27T11:00:00Z"
      }
    ],
    "id": 4,
    "created_at": "2026-03-25T11:55:00Z",
    "update_at": "2026-03-25T12:00:00Z",
    "subject": 12,
    "ai_generated": true,
    "total_hours": 24,
    "daily_study_hours": 3,
    "starting_date": "2026-03-26",
    "end_date": "2026-04-05",
    "is_completed": false,
    "topics": ["REST APIs", "database design", "background jobs"],
    "description": "A balanced plan with fundamentals first and revision near the deadline.",
    "is_creating": false,
    "is_failed": false
  }
]
```

### `GET /api/planning/plan/{plan_id}`

Success response:

- same shape as one item in the plan list response

### `POST /api/planning/plan/complete/{plan_item_id}`

Content type:

- `application/json`

Request body:

```json
{
  "start_date_time": "2026-03-27T09:00:00Z",
  "end_date_time": "2026-03-27T10:45:00Z"
}
```

Success response:

```json
{
  "id": 6,
  "created_at": "2026-03-27T10:45:00Z",
  "update_at": "2026-03-27T10:45:00Z",
  "plan_item": 9,
  "start_date_time": "2026-03-27T09:00:00Z",
  "end_date_time": "2026-03-27T10:45:00Z",
  "duration": 105
}
```

Implementation note:

- a plan item can only have one session because the relation is one-to-one

## Quizzes

### `POST /api/quiz/{subject_id}`

Content type:

- `application/json`

Recommended request body:

```json
{
  "topics": ["routing", "TCP/IP", "OSI model"],
  "difficulty_level": "mixed",
  "total_questions": 10
}
```

Success response:

```json
{
  "message": "Creating Quiz. It may take time"
}
```

Important notes:

- the route creates a quiz asynchronously
- poll `GET /api/quiz/all/{subject_id}`
- prefer question count as the readiness signal instead of `is_creating`

### `GET /api/quiz/all/{subject_id}`

Success response example:

```json
[
  {
    "attempts": [],
    "id": 21,
    "created_at": "2026-03-25T14:00:00Z",
    "update_at": "2026-03-25T14:05:00Z",
    "subject": 12,
    "topics": ["routing", "TCP/IP", "OSI model"],
    "difficulty_level": "mixed",
    "total_questions": 10,
    "is_creating": false,
    "is_failed": false,
    "ai_report": "",
    "ai_report_creating": false
  }
]
```

### `GET /api/quiz/attempt/{quiz_id}`

Success response example:

```json
{
  "questions": [
    {
      "options": [
        {
          "id": 101,
          "created_at": "2026-03-25T14:05:00Z",
          "update_at": "2026-03-25T14:05:00Z",
          "question": 55,
          "text": "Network layer",
          "is_correct": true
        }
      ],
      "id": 55,
      "created_at": "2026-03-25T14:05:00Z",
      "update_at": "2026-03-25T14:05:00Z",
      "quiz": 21,
      "question_text": "Which OSI layer handles routing?",
      "explanation": "Routing is a network-layer responsibility.",
      "difficulty": "medium",
      "topic": "routing",
      "question_type": "single"
    }
  ],
  "id": 21,
  "created_at": "2026-03-25T14:00:00Z",
  "update_at": "2026-03-25T14:05:00Z",
  "subject": 12,
  "topics": ["routing", "TCP/IP", "OSI model"],
  "difficulty_level": "mixed",
  "total_questions": 10,
  "is_creating": false,
  "is_failed": false,
  "ai_report": "",
  "ai_report_creating": false
}
```

### `POST /api/quiz/submit/{quiz_id}`

Content type:

- `application/json`

Request body:

```json
{
  "answers": [
    {
      "question_id": 55,
      "option_id": 101
    },
    {
      "question_id": 56,
      "option_id": 106
    }
  ],
  "time_taken": 480
}
```

Success response:

```json
{
  "id": 8,
  "created_at": "2026-03-25T14:20:00Z",
  "update_at": "2026-03-25T14:20:00Z",
  "quiz": 21,
  "score": 7,
  "total_score": 10,
  "time_taken": 480
}
```

Important notes:

- the backend expects exactly one submitted answer per quiz question
- invalid question or option mappings can return a generic failure response

### `POST /api/quiz/report/{quiz_id}`

Purpose:

- enqueue AI quiz performance reporting

Success response:

```json
{
  "message": "Creating Quiz AI Report. It may take time"
}
```

Current implementation note:

- this endpoint is documented for completeness, but the current background path is not fully reliable yet

## Common Integration Notes

- Use `credentials: "include"` for browser requests.
- Error shapes are not yet standardized.
- JSON fields may appear as arrays or objects depending on the resource and AI output.
