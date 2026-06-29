from app.services.groq_client import ask_groq
import json

def _normalize_score(score):
    """
    Normalize the score to an integer in the range 0-100.
    
    Handles various formats the model might return:
    - 0-100 integers (e.g., 45) → kept as-is
    - 0.0-1.0 floats (e.g., 0.45) → multiplied by 100
    - Strings (e.g., "45" or "0.45") → parsed and normalized
    - Out-of-range values → clamped to 0-100
    """
    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0
    
    if 0.0 <= score <= 1.0:
        # Model returned a fraction (0-1 range) instead of percentage
        score = score * 100
    elif score > 100:
        score = 100
    elif score < 0:
        score = 0
    
    return int(round(score))


def run_ats_agent(
    resume, 
    jd
):
    
    prompt = f"""
You are an ATS Evaluation Agent.
Score the candidate's resume against the job description.
Return ONLY valid JSON with these exact keys:
- score (integer 0-100)
- missing_keywords (array of strings)
- strengths (array of strings)
- suggestions (array of strings)

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Return ONLY the JSON object, no other text.
"""

    response = ask_groq(prompt, json_mode=True)

    if not response or not response.strip():
        return {
            "score": 0, "missing_keywords": [], "strengths": [], "suggestions": ["Empty ATS response"]
        }

    try:
        result = json.loads(response)
        
        # Normalize the score to ensure it's always an integer 0-100
        if "score" in result:
            result["score"] = _normalize_score(result["score"])
        
        # Ensure all required keys exist with proper types
        result.setdefault("missing_keywords", [])
        result.setdefault("strengths", [])
        result.setdefault("suggestions", [])
        
        return result
        
    except Exception:
        return {
            "score": 0, "missing_keywords": [], "strengths": [], "suggestions": ["Unable to parse ATS response"]
        }
        


    