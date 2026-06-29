"""
NEW FEATURE: Salary Negotiation Coach Agent
Generates negotiation scripts, market context, and counter-offer strategies
based on the role, offer details, and candidate's resume experience.
"""
from app.services.groq_client import ask_groq
import json


def run_salary_agent(
    resume: str,
    jd: str,
    job_title: str,
    company_name: str,
    current_offer: str = "",
    current_salary: str = "",
    location: str = "",
    years_experience: str = ""
) -> dict:
    """
    Generate salary negotiation advice and scripts.
    
    Returns dict with:
    - market_context: estimated salary range for the role
    - negotiation_scripts: scripts for different scenarios (email, phone, counter-offer)
    - talking_points: key strengths to highlight during negotiation
    - questions_to_ask: questions about benefits, equity, growth
    - strategy_tips: general negotiation strategy advice
    - walkaway_point: when and how to walk away
    """
    prompt = f"""
You are a Salary Negotiation Coach Agent. Provide expert negotiation advice.

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{jd}

ROLE: {job_title}
COMPANY: {company_name}
CURRENT OFFER/SALARY INFO: {current_offer}
CURRENT SALARY: {current_salary}
LOCATION: {location}
YEARS OF EXPERIENCE: {years_experience}

Provide comprehensive salary negotiation guidance. Return ONLY valid JSON with these exact keys:
- market_context (string - estimated market range and factors affecting it)
- negotiation_scripts (object with string keys: "email_script" for initial email, "phone_script" for phone conversation, "counter_offer_script" for presenting counter-offer)
- talking_points (array of strings - 4-6 key strengths and achievements to highlight)
- questions_to_ask (array of strings - 4-6 questions about benefits, equity, growth, remote work, etc.)
- strategy_tips (array of strings - 4-6 strategic tips for the negotiation process)
- walkaway_point (string - advice on when to consider walking away and how to do it professionally)

Return ONLY the JSON object, no other text.
"""
    response = ask_groq(prompt, json_mode=True)

    if not response or not response.strip():
        return _default_salary_response()

    try:
        result = json.loads(response)
        default = _default_salary_response()
        for key in default:
            result.setdefault(key, default[key])
        return result
    except Exception:
        return _default_salary_response()


def _default_salary_response() -> dict:
    return {
        "market_context": "Unable to determine market context. Research on Glassdoor, Levels.fyi, and LinkedIn for current market rates.",
        "negotiation_scripts": {
            "email_script": "Subject: Job Offer - [Job Title] - [Your Name]\n\nDear [Hiring Manager],\n\nThank you so much for the offer. I'm very excited about the opportunity to join [Company Name] and contribute to [specific project/team].\n\nAfter reviewing the offer carefully, I was hoping to discuss the compensation package. Based on my research and experience, I believe a salary of [target number] would be more aligned with market rates for this role.\n\nI'm very enthusiastic about this position and hope we can find a mutually agreeable solution.\n\nBest regards,\n[Your Name]",
            "phone_script": "Thank you for the offer - I'm really excited about this opportunity. I was hoping we could discuss the compensation package. Based on my experience with [key achievement] and market research, I was thinking something in the range of [X] would be more appropriate. I'm confident I can deliver strong results in this role and want to make sure the compensation reflects that.",
            "counter_offer_script": "I'm very interested in this role and believe my skills in [key area] align well with what you need. Based on my X years of experience, my track record of [achievement], and market rates for similar positions, I was hoping we could adjust the offer to [target number]. Is there flexibility in the budget for this role?"
        },
        "talking_points": [
            "Highlight specific achievements and metrics from your resume",
            "Emphasize unique skills that differentiate you from other candidates",
            "Reference the value you'll bring to the company's specific challenges",
            "Mention relevant certifications, education, or specialized training"
        ],
        "questions_to_ask": [
            "What is the bonus structure and how is it calculated?",
            "Are there equity or stock options included?",
            "What does the benefits package include (health, dental, 401k matching)?",
            "Is there flexibility for remote work or hybrid arrangements?",
            "What are the opportunities for professional development and growth?",
            "How is performance reviewed and what does the promotion timeline look like?"
        ],
        "strategy_tips": [
            "Always get the offer in writing before negotiating",
            "Research market rates before the conversation",
            "Practice your script out loud before the call",
            "Focus on the value you bring, not your personal needs",
            "Be professional and collaborative, not confrontational",
            "Consider total compensation, not just base salary"
        ],
        "walkaway_point": "Know your minimum acceptable number before the conversation starts. If the offer doesn't meet your minimum after good-faith negotiation, politely decline: 'Thank you for the offer, but after careful consideration, I don't think this is the right fit at this time. I wish you the best in finding the right candidate.'"
    }