from app.services.groq_client import ask_groq

def run_cover_agent(
    resume, 
    jd
):
    
    prompt = f"""
You are a Cover Letter Writing Agent.

Task:
Draft a professional, one-page cover letter tailored to the job description.

Requirements:
- Use the resume details provided
- Align with the JD responsibilities and keywords
- Keep tone professional, concise, and ATS-friendly
- Length: 1 page

Interactivity:
- Ask clarifying questions before drafting (e.g., preferred tone: formal vs. friendly, highlight specific achievements, company values to emphasize)
- Provide 2-3 alternative opening paragraphs for user choice
- Allow user to regenerate specific sections (intro, body, closing) without rewriting the whole letter

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""

    return ask_groq(prompt)
