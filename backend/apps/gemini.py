import json
import re
from collections import defaultdict
from typing import Any, Iterable

import google.generativeai as genai
from django.conf import settings


class GeminiAPIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    def request_gemini(self,contents):
        response = self.model.generate_content(contents)
        
        text = self._extract_text(response)

        return self._parse_json(text)

    def request_gemini_text(self, contents):
        response = self.model.generate_content(contents)
        return self._extract_text(response)

    def run_analyze_subject(self, subject, subject_files: Iterable[Any] | None = None):

        prompt = self.subject_analyze_prompt(subject)

        contents = [prompt]

        if subject_files:
            for file in subject_files:
                if getattr(file, "file", None):
                    uploaded = genai.upload_file(path=file.file.path)
                    contents.append(uploaded)

        return self.request_gemini(contents)

    def subject_analyze_prompt(self, subject, subject_files: Iterable[Any] | None = None) -> str:
        files_text = self._build_file_context(subject_files)

        return f"""
            You are an academic study assistant.
            Analyze the provided study material and produce structured study insights for a student.

            User Input Fields:
            - title: {subject.title}
            - description: {subject.description}
            - goal: {subject.goal}
            - deadline: {subject.deadline}
            - attached_files:
            {files_text}

            Return ONLY valid JSON (no markdown, no explanation, no extra text) with this exact structure:

            {{
            "summary": "short, clear explanation of core concepts",
            "topics": ["main topic 1", "main topic 2"],
            "subtopics": [
                {{
                "topic": "topic name",
                "subtopics": ["subtopic 1", "subtopic 2"]
                }}
            ],
            "key_points": ["important concept or takeaway"],
            "concepts": [
                {{
                "term": "concept name",
                "definition": "short explanation"
                }}
            ],
            "topic_wise_priority": [
                {{
                "topic": "topic name",
                "priority": "low|medium|high"
                }}
            ],
            "recommended_focus": ["topics the student should focus on more"],
            "difficulty_level": "low|medium|high",
            "estimated_hours": number
            }}

            Rules:
            - Focus only on educational content derived from the input.
            - Use attached file content as the primary source when available.
            - Keep "summary" under 120 words.
            - Provide 3–8 items for topics when possible.
            - Provide 2–5 subtopics per topic when possible.
            - Key points should capture the most important learning ideas.
            - Concepts should include important terminology students must understand.
            - topic_wise_priority should reflect importance for achieving the user's goal.
            - "high" priority topics should be essential or foundational.
            - recommended_focus should highlight topics that require deeper attention.
            - If attached files lack content, infer information from title, description, goal, and deadline.
            - difficulty_level should represent the overall complexity of the subject.
            - estimated_hours must be a realistic number for an average student.
            """

    def run_quiz_creation(self, subject, quiz):
        subject_files = list(subject.files.all())
        previous_quizzes = list(
            subject.quizzes.exclude(id=quiz.id)
            .prefetch_related(
                "questions__options",
                "attempts__answers__question",
                "attempts__answers__selected_option",
            )
            .order_by("created_at")
        )

        prompt = self.subject_quiz_prompt(
            subject=subject,
            quiz=quiz,
            previous_quizzes=previous_quizzes,
            subject_files=subject_files,
        )

        contents = [prompt]
        for file in subject_files:
            if getattr(file, "file", None):
                uploaded = genai.upload_file(path=file.file.path)
                contents.append(uploaded)

        return self.request_gemini(contents)

    def subject_quiz_prompt(
        self,
        subject,
        quiz,
        previous_quizzes: Iterable[Any] | None = None,
        subject_files: Iterable[Any] | None = None,
    ) -> str:
        context = {
            "subject": self._build_subject_context(subject),
            "subject_analysis": self._build_subject_analysis_context(subject),
            "attached_files": self._build_subject_files_context(subject_files),
            "requested_quiz": self._build_quiz_request_context(quiz),
            "previous_quiz_summary": self._build_previous_quiz_summary(previous_quizzes),
            "previous_quizzes": self._build_previous_quizzes_context(previous_quizzes),
        }

        requested_topics = self._normalize_topics(getattr(quiz, "topics", []))
        topic_instruction = ", ".join(requested_topics) if requested_topics else "use the strongest subject topics"

        return f"""
            You are an expert educational quiz designer inside an AI study planner.
            Create a new quiz that fits the subject, helps the learner progress, and clearly avoids repeating old quiz activity.

            Use the JSON context below as the complete source of truth.
            The `previous_quizzes` block is mandatory history and must influence the new quiz.

            CONTEXT:
            {json.dumps(context, indent=2, ensure_ascii=True, default=str)}

            Return ONLY valid JSON with this exact structure:
            {{
              "questions": [
                {{
                  "question_text": "clear question",
                  "explanation": "teaching explanation for why the answer is correct",
                  "difficulty": "low|medium|high",
                  "topic": "one topic name",
                  "question_type": "single|multiple",
                  "options": [
                    {{
                      "text": "answer option",
                      "is_correct": true
                    }}
                  ]
                }}
              ]
            }}

            Rules:
            - Create exactly {quiz.total_questions} questions.
            - The quiz must stay aligned with the requested topics: {topic_instruction}.
            - Use subject details, subject analysis, and attached files as the primary knowledge source.
            - Treat every previous quiz as existing activity for this subject.
            - Do not repeat the same question text, near-duplicate wording, same fact pattern, or same answer ordering from previous quizzes.
            - Use previous attempt performance to identify weak areas; if the learner struggled before, ask a fresh follow-up question from a different angle.
            - If the learner already mastered a concept in previous quizzes, reduce repetition and move slightly deeper.
            - Cover gaps that were not asked before whenever possible.
            - Each question must have at least 4 options.
            - If question_type is "single", exactly 1 option must have is_correct=true.
            - If question_type is "multiple", at least 2 options must have is_correct=true.
            - Keep explanations concise, accurate, and actually helpful for learning.
            - Mix difficulty intelligently using low, medium, and high based on the subject complexity and past activity.
            - Keep topics accurate to the subject and prefer the topic names already present in the context.
            - Do not include markdown, commentary, or any text outside the JSON object.
            """

    def run_ai_quiz_report(self, quiz):
        prompt = self.quiz_report_prompt(quiz)
        return self.request_gemini_text([prompt])

    def quiz_report_prompt(self, quiz) -> str:
        context = {
            "subject": self._build_subject_context(quiz.subject),
            "subject_analysis": self._build_subject_analysis_context(quiz.subject),
            "quiz": self._build_quiz_context(quiz),
            "quiz_attempt_summary": self._build_quiz_attempt_summary(quiz),
        }

        return f"""
            You are an expert learning coach and assessment analyst.
            Review the quiz performance and write one detailed plain-text report for the student.

            Use this JSON context as the source of truth:
            {json.dumps(context, indent=2, ensure_ascii=True, default=str)}

            Main goals:
            - Explain what parts of the subject this quiz covered.
            - Identify the topics, concepts, and skills the student seems to understand well.
            - Identify the parts where the student needs more attention, revision, or practice.
            - Look for mistake patterns across all quiz attempts, including weak topics, repeated confusion, and accuracy gaps.
            - Explain what the student should study next and why.
            - If there are no attempts or too little evidence, say that clearly and still describe the quiz coverage.

            Output rules:
            - Return plain detailed text only.
            - Return a single report and nothing else.
            - Do not return JSON.
            - Do not use markdown code blocks.
            - Do not add labels like "Report:" or "Summary:" before the response.
            """

    def _build_file_context(self, subject_files: Iterable[Any] | None) -> str:
        if not subject_files:
            return "- none"

        lines: list[str] = []
        for idx, file_obj in enumerate(subject_files, start=1):
            title = (getattr(file_obj, "title", "") or "").strip()
            description = (getattr(file_obj, "description", "") or "").strip()
            file_type = (getattr(file_obj, "file_type", "") or "").strip()
            lines.append(
                f"  {idx}. title='{title}', description='{description}', file_type='{file_type}'"
            )

        if not lines:
            return "- none"
        return "\n".join(lines)

    def _build_subject_context(self, subject) -> dict[str, Any]:
        return {
            "id": getattr(subject, "id", None),
            "title": getattr(subject, "title", ""),
            "description": getattr(subject, "description", ""),
            "goal": getattr(subject, "goal", ""),
            "deadline": str(getattr(subject, "deadline", "") or ""),
            "status": getattr(subject, "status", ""),
        }

    def _build_subject_analysis_context(self, subject) -> dict[str, Any] | None:
        subject_analyze = getattr(subject, "subject_analyze", None)

        if not subject_analyze:
            return None

        return {
            "summary": getattr(subject_analyze, "summary", ""),
            "difficulty_level": getattr(subject_analyze, "difficulty_level", ""),
            "topics": getattr(subject_analyze, "topics", []),
            "subtopics": getattr(subject_analyze, "subtopics", []),
            "concepts": getattr(subject_analyze, "concepts", []),
            "topic_wise_priority": getattr(subject_analyze, "topic_wise_priority", []),
            "key_points": getattr(subject_analyze, "key_points", []),
            "recommended_focus": getattr(subject_analyze, "recommended_focus", []),
            "estimated_hours": getattr(subject_analyze, "estimated_hours", None),
        }

    def _build_subject_files_context(
        self, subject_files: Iterable[Any] | None
    ) -> list[dict[str, str]]:
        if not subject_files:
            return []

        file_context: list[dict[str, str]] = []

        for file_obj in subject_files:
            file_context.append(
                {
                    "title": (getattr(file_obj, "title", "") or "").strip(),
                    "description": (getattr(file_obj, "description", "") or "").strip(),
                    "file_type": (getattr(file_obj, "file_type", "") or "").strip(),
                }
            )

        return file_context

    def _build_quiz_request_context(self, quiz) -> dict[str, Any]:
        return {
            "id": getattr(quiz, "id", None),
            "topics": self._normalize_topics(getattr(quiz, "topics", [])),
            "total_questions": getattr(quiz, "total_questions", 0),
            "difficulty_level": getattr(quiz, "difficulty_level", None),
            "question_type":"single"
        }

    def _build_quiz_context(self, quiz) -> dict[str, Any]:
        return {
            "id": getattr(quiz, "id", None),
            "topics": self._normalize_topics(getattr(quiz, "topics", [])),
            "total_questions": getattr(quiz, "total_questions", 0),
            "difficulty_level": getattr(quiz, "difficulty_level", None),
            "created_at": str(getattr(quiz, "created_at", "") or ""),
            "questions": [
                {
                    "question_text": question.question_text,
                    "explanation": question.explanation,
                    "difficulty": question.difficulty,
                    "topic": question.topic,
                    "question_type": question.question_type,
                    "options": [
                        {
                            "text": option.text,
                            "is_correct": option.is_correct,
                        }
                        for option in question.options.all()
                    ],
                }
                for question in quiz.questions.all()
            ],
            "attempts": [
                {
                    "score": attempt.score,
                    "total_score": attempt.total_score,
                    "time_taken": attempt.time_taken,
                    "answers": [
                        {
                            "question_text": answer.question.question_text,
                            "topic": answer.question.topic,
                            "selected_option": answer.selected_option.text,
                            "is_correct": answer.is_correct,
                        }
                        for answer in attempt.answers.all()
                    ],
                }
                for attempt in quiz.attempts.all()
            ],
        }

    def _build_previous_quizzes_context(
        self, previous_quizzes: Iterable[Any] | None
    ) -> list[dict[str, Any]]:
        if not previous_quizzes:
            return []

        return [self._build_quiz_context(previous_quiz) for previous_quiz in previous_quizzes]

    def _build_previous_quiz_summary(
        self, previous_quizzes: Iterable[Any] | None
    ) -> dict[str, Any]:
        if not previous_quizzes:
            return {
                "total_previous_quizzes": 0,
                "topics_seen": [],
                "topic_accuracy": [],
                "attempted_quizzes": 0,
            }

        previous_quizzes = list(previous_quizzes)
        topic_stats: dict[str, dict[str, int]] = defaultdict(
            lambda: {"correct": 0, "total": 0}
        )
        topics_seen: set[str] = set()
        attempted_quizzes = 0

        for previous_quiz in previous_quizzes:
            topics_seen.update(self._normalize_topics(getattr(previous_quiz, "topics", [])))

            attempts = list(previous_quiz.attempts.all())
            if attempts:
                attempted_quizzes += 1

            for attempt in attempts:
                for answer in attempt.answers.all():
                    topic = (getattr(answer.question, "topic", "") or "").strip()
                    if not topic:
                        continue
                    topic_stats[topic]["total"] += 1
                    if answer.is_correct:
                        topic_stats[topic]["correct"] += 1

        topic_accuracy = []
        for topic, stats in sorted(topic_stats.items(), key=lambda item: item[0].lower()):
            total = stats["total"]
            accuracy = round(stats["correct"] / total, 3) if total else 0
            topic_accuracy.append(
                {
                    "topic": topic,
                    "correct_answers": stats["correct"],
                    "total_answers": total,
                    "accuracy": accuracy,
                }
            )

        return {
            "total_previous_quizzes": len(previous_quizzes),
            "topics_seen": sorted(topics_seen),
            "topic_accuracy": topic_accuracy,
            "attempted_quizzes": attempted_quizzes,
        }

    def _build_quiz_attempt_summary(self, quiz) -> dict[str, Any]:
        attempts = list(quiz.attempts.all())
        if not attempts:
            return {
                "total_attempts": 0,
                "average_score": None,
                "best_score": None,
                "latest_score": None,
                "topic_accuracy": [],
            }

        topic_stats: dict[str, dict[str, int]] = defaultdict(
            lambda: {"correct": 0, "total": 0}
        )
        scores: list[float] = []

        for attempt in attempts:
            total_score = getattr(attempt, "total_score", 0) or 0
            score = getattr(attempt, "score", 0) or 0
            percentage = round((score / total_score) * 100, 2) if total_score else 0
            scores.append(percentage)

            for answer in attempt.answers.all():
                topic = (getattr(answer.question, "topic", "") or "").strip()
                if not topic:
                    continue
                topic_stats[topic]["total"] += 1
                if answer.is_correct:
                    topic_stats[topic]["correct"] += 1

        topic_accuracy = []
        for topic, stats in sorted(topic_stats.items(), key=lambda item: item[0].lower()):
            total = stats["total"]
            accuracy = round((stats["correct"] / total) * 100, 2) if total else 0
            topic_accuracy.append(
                {
                    "topic": topic,
                    "correct_answers": stats["correct"],
                    "total_answers": total,
                    "accuracy_percentage": accuracy,
                }
            )

        latest_attempt = max(
            attempts,
            key=lambda attempt: str(getattr(attempt, "created_at", "") or ""),
        )
        latest_total = getattr(latest_attempt, "total_score", 0) or 0
        latest_score = getattr(latest_attempt, "score", 0) or 0

        return {
            "total_attempts": len(attempts),
            "average_score": round(sum(scores) / len(scores), 2),
            "best_score": max(scores),
            "latest_score": round((latest_score / latest_total) * 100, 2)
            if latest_total
            else 0,
            "topic_accuracy": topic_accuracy,
        }

    def _normalize_topics(self, topics: Any) -> list[str]:
        if topics is None:
            return []
        if isinstance(topics, list):
            return [str(topic).strip() for topic in topics if str(topic).strip()]
        if isinstance(topics, tuple):
            return [str(topic).strip() for topic in topics if str(topic).strip()]
        if isinstance(topics, dict):
            normalized: list[str] = []
            for key, value in topics.items():
                key_text = str(key).strip()
                if key_text:
                    normalized.append(key_text)
                if isinstance(value, list):
                    normalized.extend(
                        str(item).strip() for item in value if str(item).strip()
                    )
                elif value:
                    normalized.append(str(value).strip())
            return normalized

        topic_text = str(topics).strip()
        return [topic_text] if topic_text else []

    def _extract_text(self, response):

        if response.text:
            return response.text.strip()

        for c in response.candidates:
            for part in c.content.parts:
                if hasattr(part, "text"):
                    return part.text.strip()

        raise ValueError("No text in Gemini response")

    def _parse_json(self, text):

        text = re.sub(r"```json|```", "", text).strip()

        try:
            return json.loads(text)
        except Exception:

            start = text.find("{")
            end = text.rfind("}")

            if start == -1 or end == -1:
                raise ValueError("Invalid JSON from Gemini")

            return json.loads(text[start:end + 1])
