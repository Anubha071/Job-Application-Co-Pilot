from app.services.groq_client import ask_groq

def run_resume_agent(
    resume,
    jd,
    fit_analysis
):
    
    prompt = f"""
You are a Resume Rewriting Agent.

Task:
Rewrite the resume to improve clarity, professionalism, and ATS compatibility.

Requirements:
- Keep the same experiences and companies
- Improve wording for stronger impact
- Integrate JD keywords seamlessly into bullets and skills (no keyword stuffing)
- Maintain professional, concise tone
- Output in structured resume format: Header, Experience, Education, Skills

FIT ANALYSIS:
{fit_analysis}

ORIGINAL RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""

    return ask_groq(prompt)