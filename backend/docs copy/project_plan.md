# Delivery Roadmap

This roadmap is based on the current implementation, not a greenfield design.

## Already Implemented

- Google-based login bootstrap
- JWT creation and refresh logic
- subject CRUD
- subject file upload
- AI subject analysis
- AI study plan generation
- AI quiz generation
- quiz attempt submission
- failed-task logging

## Highest-Priority Next Work

### Production readiness

- move all settings and secrets to environment variables
- rotate exposed secrets
- configure static file handling for production
- add structured logging and deployment secrets management

### Authentication hardening

- set secure cookies server-side on login and refresh
- add logout endpoint
- align refresh and access handling with a consistent browser contract

### Quiz reliability

- fix quiz generation status persistence
- fix AI report task argument mismatch
- reset `ai_report_creating` correctly on success

### API usability

- include subject IDs in subject responses
- return created plan and quiz identifiers from async create endpoints
- standardize error responses

### Quality

- add tests for planning flows
- add tests for quiz generation and submission
- add tests for permissions and failure modes

## Nice-To-Have Follow-Up Work

- admin workflows for reviewing failed tasks
- analytics endpoints for dashboards
- request correlation IDs for async jobs
- rate limiting around AI endpoints
- stronger API versioning strategy
