"""
NEW FEATURE: Salary Negotiation Coach Routes
Provides endpoints for salary negotiation guidance.
- POST /salary-coach/generate: Generate negotiation advice for a role
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.application import Application
from app.agents.salary_agent import run_salary_agent
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/salary-coach",
    tags=["Salary Coach"]
)


class SalaryCoachRequest(BaseModel):
    application_id: int
    current_offer: str = ""
    current_salary: str = ""
    location: str = ""
    years_experience: str = ""


@router.post("/generate")
def generate_salary_advice(
    req: SalaryCoachRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Generate salary negotiation advice for a specific application.
    Uses the application's resume, JD, and user-provided offer details.
    """
    application = db.query(Application).filter(
        Application.id == req.application_id,
        Application.user_id == user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    result = run_salary_agent(
        resume=application.resume_text or "",
        jd=application.job_description or "",
        job_title=application.job_title or "",
        company_name=application.company_name or "",
        current_offer=req.current_offer,
        current_salary=req.current_salary,
        location=req.location,
        years_experience=req.years_experience
    )
    
    return {
        "success": True,
        "market_context": result["market_context"],
        "negotiation_scripts": result["negotiation_scripts"],
        "talking_points": result["talking_points"],
        "questions_to_ask": result["questions_to_ask"],
        "strategy_tips": result["strategy_tips"],
        "walkaway_point": result["walkaway_point"]
    }