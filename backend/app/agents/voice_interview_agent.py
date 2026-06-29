"""
NEW FEATURE: Voice Mock Interview Agent
Provides voice-based mock interview practice with LLM grading.
- Takes a question + candidate's spoken answer (transcribed to text)
- Evaluates the answer and provides structured feedback
- Returns a score, strengths, weaknesses, and a model answer
"""
from app.services.groq_client import ask_groq
import json


def run_voice_interview_agent(question: str, candidate_answer: str, resume: str, jd: str) -> dict:
    """
    Run the voice interview agent to grade a candidate's spoken answer.
    
    Args:
        question: The interview question asked
        candidate_answer: The candidate's transcribed spoken answer
        resume: The candidate's resume text
        jd: The job description text
    
    Returns:
        dict with keys: score, feedback, strengths, weaknesses, model_answer
    """
    prompt = f"""
You are a Voice Interview Coach Agent. Evaluate the candidate's spoken answer to an interview question.

JOB DESCRIPTION:
{jd}

RESUME:
{resume}

INTERVIEW QUESTION:
{question}

CANDIDATE'S SPOKEN ANSWER (transcribed from speech):
{candidate_answer}

Evaluate the answer based on:
1. Relevance to the question
2. Use of STAR format (Situation, Task, Action, Result)
3. Specificity and use of resume details
4. Clarity and structure
5. Alignment with JD requirements and keywords

Return ONLY valid JSON with these exact keys:
- score (integer 0-100)
- feedback (string - overall assessment, 2-3 sentences)
- strengths (array of strings - 2-3 strengths)
- weaknesses (array of strings - 2-3 areas to improve)
- model_answer (string - a well-structured sample answer using STAR format)

Return ONLY the JSON object, no other text.
"""
    response = ask_groq(prompt, json_mode=True)

    if not response or not response.strip():
        return {
            "score": 0,
            "feedback": "Unable to evaluate answer.",
            "strengths": [],
            "weaknesses": [],
            "model_answer": ""
        }

    try:
        result = json.loads(response)
        # Normalize score
        try:
            score = float(result.get("score", 0))
            if 0.0 <= score <= 1.0:
                score = score * 100
            result["score"] = max(0, min(100, int(round(score))))
        except (TypeError, ValueError):
            result["score"] = 0
        
        result.setdefault("feedback", "")
        result.setdefault("strengths", [])
        result.setdefault("weaknesses", [])
        result.setdefault("model_answer", "")
        
        return result
    except Exception:
        return {
            "score": 0,
            "feedback": "Unable to parse evaluation response.",
            "strengths": [],
            "weaknesses": [],
            "model_answer": ""
        }


def generate_voice_question(resume: str, jd: str, difficulty: str = "moderate") -> dict:
    """
    Generate a mock interview question for voice practice.
    
    Args:
        resume: The candidate's resume
        jd: The job description
        difficulty: "easy", "moderate", or "challenging"
    
    Returns:
        dict with keys: question, type (technical/behavioral), tips
    """
    prompt = f"""
You are an Interview Question Generator for voice mock interviews.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

DIFFICULTY LEVEL: {difficulty}

Generate a single interview question that:
- Matches the difficulty level specified
- Is either technical (role-specific) or behavioral
- Is grounded in the candidate's actual resume experience
- Relates to the job description requirements

Return ONLY valid JSON with these exact keys:
- question (string - the interview question)
- type (string - "technical" or "behavioral")
- tips (string - brief advice on how to structure the answer)

Return ONLY the JSON object, no other text.
"""
    response = ask_groq(prompt, json_mode=True)

    try:
        result = json.loads(response) if response and response.strip() else {}
        result.setdefault("question", "Tell me about yourself and why you're a good fit for this role.")
        result.setdefault("type", "behavioral")
        result.setdefault("tips", "Use STAR format: Situation, Task, Action, Result.")
        return result
    except Exception:
        return {
            "question": "Tell me about yourself and why you're a good fit for this role.",
            "type": "behavioral",
            "tips": "Use STAR format: Situation, Task, Action, Result."
        }