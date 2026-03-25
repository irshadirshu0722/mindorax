# Project Analysis

## Executive Summary

The repository already has a solid domain split and a clear product direction. The main backend foundations are in place:

- authentication
- subject management
- file uploads
- AI subject analysis
- AI study plan generation
- AI quiz generation
- quiz attempt tracking
- failed background-task logging

The biggest gaps are not missing modules. They are operational and contract-level issues:

- hard-coded settings and secrets
- token flow mismatch between login and authenticated requests
- partial async status visibility for the frontend
- thin automated test coverage
- a few task-level bugs in the quiz-report flow

## Module Review

### `apps.users`

- Handles Google token verification and JWT generation.
- The public login endpoint returns `access_token` and `refresh_token` in JSON.
- Middleware later expects `access_token` to be present in cookies.
- Refresh also expects `refresh_token` in cookies.

### `apps.subjects`

- Supports subject CRUD, file upload, and async subject analysis.
- Subject analysis stores a structured `SubjectAnalyze` record with summary, topics, subtopics, concepts, priorities, and estimated hours.
- The response schema is useful for UI rendering, but it does not expose the subject `id` or analysis flags.

### `apps.planning`

- Creates a `StudyPlan` record immediately, then fills it asynchronously with plan items from Gemini.
- The planning domain is one of the stronger parts of the project because it persists both the requested plan and the generated sessions.
- A frontend can reliably poll plan readiness using `is_creating` and `is_failed`.

### `apps.quizzes`

- Supports quiz creation, listing, retrieval, submission, and AI report requests.
- The question and attempt data model is strong enough for reporting and future analytics.
- There are currently reliability issues in the async status flow and AI report task implementation.

### `apps.logs`

- Failed Celery tasks are stored in `FailedTaskAlert`.
- This is a good production-minded addition and gives the project a useful operational audit trail.

## Architectural Strengths

- Clear app boundaries by domain
- Controller -> service -> repository separation
- Background-task retries with dead-letter style persistence
- Response schemas for most major resources
- Reasonable use of JSON fields for AI-generated structures

## Highest-Risk Gaps

1. Environment and secret management are not production safe yet.
2. Authentication contract is inconsistent for browser clients.
3. Quiz background status fields are not currently reliable for frontend polling.
4. Quiz AI report generation has a task/service signature mismatch.
5. Test coverage is very limited outside a small auth and subject smoke test.

## What This Documentation Update Delivers

- accurate architecture docs
- detailed API request and response docs
- frontend integration guidance
- Docker and docker-compose support files
- contribution and security docs
- quick-run commands through `Makefile`

## Recommended Next Engineering Iteration

1. Move settings to environment variables and rotate exposed secrets.
2. Make login and refresh set secure cookies server-side.
3. Fix quiz async lifecycle flags to update the `Quiz` model, not `Subject`.
4. Fix the quiz AI report task call so it passes the quiz instance correctly.
5. Expand tests around planning, quizzes, and permissions.
