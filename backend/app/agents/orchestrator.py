from app.agents.fit_agent import run_fit_agent
from app.agents.resume_agent import run_resume_agent
from app.agents.cover_agent import run_cover_agent
from app.agents.interview_agent import run_interview_agent
from app.agents.ats_score import run_ats_agent

def run_pipeline(
    resume, 
    jd
):
    
    fit = run_fit_agent(
        resume,
        jd
    )
    
    rewritten_resume = run_resume_agent(
        resume,
        jd,
        fit
    )
    
    cover = run_cover_agent(
        resume,
        jd
    )
    
    interview = run_interview_agent(
        resume,
        jd
    )
    
    ats_score = run_ats_agent(
        resume,
        jd
    )
    
    return {
        "fit_analysis": fit,
        "resume_rewrite": rewritten_resume,
        "cover_letter": cover,
        "interview_pack": interview,
        "ats_score": ats_score
    }