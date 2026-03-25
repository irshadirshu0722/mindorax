# Known Issues And Constraints

This document lists important behavior the frontend, integrators, and maintainers should know about before building on top of the current backend.

## 1. Hard-Coded Runtime Configuration

The Django settings currently hard-code:

- `SECRET_KEY`
- PostgreSQL host, database, username, and password
- Redis cache and broker URLs
- Google client ID
- Gemini API key

Impact:

- not safe for public production use
- difficult to promote between environments
- Docker has to mirror the same values instead of reading clean environment config

## 2. Login Returns Tokens, Middleware Reads Cookies

Current behavior:

- `POST /api/auth/google-login` returns tokens in the JSON response body
- `JWTMiddleware` reads `access_token` from cookies
- `GET /api/auth/refresh` reads `refresh_token` from cookies

Impact:

- a frontend must persist both tokens into cookies after login
- a pure SPA must do that manually, which is less secure than server-set `HttpOnly` cookies

## 3. Subject Responses Do Not Include Subject ID

`SubjectResponse` exposes:

- `title`
- `description`
- `goal`
- `deadline`
- `status`
- `files`
- `subject_analyze`

It does not expose:

- `id`
- `is_analyzing`
- `is_failed_analyze`

Impact:

- clients cannot get the created subject ID directly from the create response
- analysis progress must be inferred by checking whether `subject_analyze` is present

## 4. Create Endpoints For Plans And Quizzes Are Fire-And-Poll

Current behavior:

- study plan creation returns only a message
- quiz creation returns only a message

Impact:

- frontend must list plans or quizzes again to discover the created resource
- there is no request correlation ID yet

## 5. Quiz Status Flags Are Not Reliable Right Now

The quiz creation task updates status flags through `QuizService.update_creating_quiz_status`, but that method currently updates the related `Subject` instance instead of the `Quiz` instance.

Impact:

- `Quiz.is_creating` and `Quiz.is_failed` cannot be trusted as live progress indicators
- the safer readiness signal is whether `questions.length === total_questions`

## 6. Quiz AI Report Flow Is Currently Fragile

Two issues are visible in the current code path:

- the background task calls `run_ai_quiz_report()` without passing the required quiz argument
- on successful completion, `ai_report_creating` is not reset to `False`

Impact:

- treat `/api/quiz/report/{quiz_id}` as experimental until fixed
- do not rely on `ai_report_creating` becoming false after success

## 7. Dependency List Was Incomplete

The code imports:

- `google.generativeai`
- Google auth libraries
- `jwt`

Those packages were not listed in `requirements.txt` previously. This documentation update adds the missing package entries so Docker and fresh installs can build correctly.

## 8. Gemini SDK Deprecation Warning

`python manage.py check` currently emits a warning that `google.generativeai` is deprecated.

Impact:

- current functionality may still work
- the codebase should be migrated to the newer Google Gen AI SDK in a future change

## 9. Test Coverage Is Still Minimal

There are only a few tests in place today, mainly around:

- Google auth response shape
- authenticated subject creation

Impact:

- deployment confidence is limited for planning and quiz flows
- changes in async behavior need careful manual verification
