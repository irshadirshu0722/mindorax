🔐 1. USERS

Your users table is fine but should include OAuth readiness.

users
-----
id (uuid, pk)
email (unique, indexed)
name
avatar_url
oauth_provider (google)
oauth_id
created_at
updated_at

Indexes:

INDEX(email)

Reason:
Google OAuth login lookup.

📚 2. SUBJECT DOMAIN

This is the core entity.

subjects
---------
id (uuid, pk)
user_id (fk -> users)
title
description
scope_text
deadline
difficulty_level
status (active, completed, archived)

ai_summary (text)
ai_topics (jsonb)

created_at
updated_at

Indexes:

INDEX(user_id)
INDEX(status)

Why ai_topics?

AI may extract:

["arrays","linked list","trees"]

Useful for quiz generation.

📂 3. SUBJECT FILES

Your idea is correct.

But we separate file storage and extraction.

subject_files
--------------
id
subject_id (fk)
file_url
file_type
uploaded_at

Indexes:

INDEX(subject_id)
📄 4. FILE EXTRACTION

Your SubjectExtract becomes:

subject_file_extractions
-------------------------
id
file_id (fk -> subject_files)
raw_text
processed_summary
extracted_topics (jsonb)
created_at

Why?

raw_text → large text

processed_summary → condensed for AI

extracted_topics → topic extraction

AI will mostly use processed_summary.

📅 5. STUDY PLAN

Your design was good but needs slight improvement.

study_plans
------------
id
subject_id (fk)
ai_generated (boolean)
total_hours
daily_study_hours
deadline
plan_json (jsonb)
created_at

Example plan_json:

{
 "week1": ["arrays","linked list"],
 "week2": ["trees"]
}
📅 PLAN ITEMS


plan_items
-----------
id
plan_id (fk)
topic
estimated_hours
order_index
status (pending, active, completed)

Indexes:

INDEX(plan_id)
⏱️ STUDY TIMER / ACTIVITY

Your PlanActivityLog becomes:

study_sessions
---------------
id
user_id
subject_id
plan_item_id
start_time
end_time
duration_minutes
is_completed
created_at

Indexes:

INDEX(user_id)

Used for analytics.

🧠 QUIZ DOMAIN

Your structure is good but missing attempts.

Quiz
quizzes
--------
id
subject_id
topic
difficulty
total_questions
created_by_ai (boolean)
created_at

Indexes:

INDEX(subject_id)
INDEX(topic)
Quiz Questions
quiz_questions
---------------
id
quiz_id
question_text
explanation
difficulty
topic
Question Options
quiz_question_options
---------------------
id
question_id
option_text
is_correct
📝 QUIZ ATTEMPTS (CRITICAL TABLE)

You missed this but it's essential.

quiz_attempts
--------------
id
user_id
quiz_id
score
total_questions
time_taken
created_at

Indexes:

INDEX(user_id)
INDEX(quiz_id)
📝 QUESTION ATTEMPT

Tracks weak areas.

question_attempts
------------------
id
attempt_id
question_id
selected_option_id
is_correct

Now you can calculate weak topics.

📊 SUBJECT ANALYTICS (OPTIONAL CACHE TABLE)

For faster dashboard:

subject_statistics
------------------
subject_id
total_study_minutes
quiz_attempts
avg_quiz_score
coverage_percentage
last_updated

This can be updated by background tasks.