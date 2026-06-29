from app.services.groq_client import ask_groq

def run_fit_agent(
    resume, 
    jd
):
    
    prompt = f"""
    Act as a seasoned career coach and ATS specialist.  

Review the candidate’s RESUME and the JOB DESCRIPTION provided.  

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Generate a concise but impactful report that includes:  
1. Match Score (quantify alignment)  
2. Matching Skills (resume vs JD overlap)  
3. Missing Skills (critical gaps)  
4. Strengths (competitive advantages)  
5. Weaknesses (areas to improve)  
6. Keywords To Emphasize (for ATS optimization)  

Present the findings in a professional, easy‑to‑scan format suitable for recruiters and job seekers.
 
    """
    return ask_groq(prompt)