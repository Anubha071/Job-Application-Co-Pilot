from app.services.groq_client import ask_groq

def run_interview_agent(
    resume, 
    jd
):
    
    prompt = f"""
You are an Interview Preparation Agent.

Task:
Generate 10 interview questions and sample answers tailored to the resume and job description.

Requirements:
- Questions should reflect both technical and behavioral aspects
- Answers should be grounded in the candidate's resume and aligned with JD keywords
- Keep tone professional and concise
- Provide answers in STAR format (Situation, Task, Action, Result) where relevant

Interactivity:
- Offer 2-3 alternative phrasings for each question (user can choose preferred style)
- Allow user to regenerate specific answers without rewriting all
- Ask clarifying questions before drafting (e.g., "Do you want more technical or behavioral focus?")
- Provide difficulty levels (easy, moderate, challenging) so user can practice progressively

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""
    return ask_groq(prompt)