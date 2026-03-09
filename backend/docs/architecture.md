# System Architecture

## High-Level Architecture

The system follows a modular architecture separating responsibilities across layers.

Frontend
↓
API Layer (Django Ninja)
↓
Service Layer
↓
Repository Layer
↓
Database (PostgreSQL)

Supporting services include Redis and Celery for caching and background tasks.

---

# Backend Architecture

The backend follows a domain-driven modular structure.

```
apps/
  users
  subjects
  planning
  quizzes

services/
repositories/
schemas/
tasks/
utils/
```

Each layer has a specific responsibility.

---

# API Layer

Implemented using Django Ninja.

Responsibilities:

- HTTP request handling
- Input validation
- Response serialization
- Authentication enforcement

Example endpoint categories:

- Authentication
- Subjects
- Study Plans
- Quizzes
- Analytics

---

# Service Layer

Services contain the core business logic.

Examples:

- SubjectService
- StudyPlanService
- QuizGenerationService
- AIService

Responsibilities:

- Orchestrating domain logic
- AI prompt management
- Data transformation
- Validation rules

---

# Repository Layer

Repositories isolate database interactions.

Responsibilities:

- Query abstraction
- Complex filtering
- Data persistence

This separation prevents business logic from being mixed with database access.

---

# AI Integration Layer

AI is used for:

- Study plan generation
- Quiz generation
- Performance analysis

AI services operate using structured prompts and return structured JSON responses.

AI does not store state; the database is the system’s source of truth.

---

# Background Processing

Celery is used for asynchronous tasks such as:

- File text extraction
- AI summary generation
- Analytics recalculation

Redis acts as the message broker.

---

# Caching

Redis is used for:

- Frequently accessed subject data
- Dashboard statistics
- AI generation caching

---

# Authentication Flow

The system uses JWT tokens stored in HttpOnly cookies.

Authentication process:

1. User logs in via Google OAuth
2. Backend validates OAuth token
3. Backend generates JWT tokens
4. Tokens stored in HttpOnly cookies
5. Middleware validates token on each request

---

# Data Storage

Primary database: PostgreSQL

Reasons:

- Strong relational integrity
- JSON support
- Indexing capabilities
- Mature ecosystem

---

# Security Principles

- HttpOnly authentication cookies
- Secure token expiration
- Input validation using schemas
- Strict API access control
- Background processing isolation

---

# Scalability Considerations

The architecture supports scaling through:

- Stateless APIs
- Background task processing
- Redis caching
- Modular service design
