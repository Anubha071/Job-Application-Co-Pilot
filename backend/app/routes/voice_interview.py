"""
NEW FEATURE: Voice Mock Interview Routes
Provides endpoints for voice-based mock interview practice.
- POST /voice-interview/generate-question: Generate a new interview question
- POST /voice-interview/evaluate-answer: Evaluate a spoken answer
- POST /voice-interview/start-session: Start a new interview session
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.application import Application
from app.models.draft import Draft
from app.agents.voice_interview_agent import (
    run_voice_interview_agent,
    generate_voice_question
)
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/voice-interview",
    tags=["Voice Interview"]
)


class GenerateQuestionRequest(BaseModel):
    application_id: int
    difficulty: str = "moderate"  # easy, moderate, challenging


class EvaluateAnswerRequest(BaseModel):
    question: str
    candidate_answer: str
    application_id: int


class StartSessionRequest(BaseModel):
    application_id: int
    difficulty: str = "moderate"


@router.post("/generate-question")
def generate_question(
    req: GenerateQuestionRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Generate a new mock interview question grounded in the resume and JD.
    """
    # Get the application
    application = db.query(Application).filter(
        Application.id == req.application_id,
        Application.user_id == user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not application.resume_text or not application.job_description:
        raise HTTPException(status_code=400, detail="Application missing resume or job description")
    
    result = generate_voice_question(
        resume=application.resume_text,
        jd=application.job_description,
        difficulty=req.difficulty
    )
    
    return {
        "success": True,
        "question": result["question"],
        "type": result["type"],
        "tips": result["tips"]
    }


@router.post("/evaluate-answer")
def evaluate_answer(
    req: EvaluateAnswerRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Evaluate a candidate's spoken answer to an interview question.
    The answer should be transcribed text (from browser speech-to-text).
    """
    # Get the application to load resume and JD context
    application = db.query(Application).filter(
        Application.id == req.application_id,
        Application.user_id == user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    result = run_voice_interview_agent(
        question=req.question,
        candidate_answer=req.candidate_answer,
        resume=application.resume_text or "",
        jd=application.job_description or ""
    )
    
    # Save the evaluation to a revision for history tracking
    draft = db.query(Draft).filter(
        Draft.application_id == application.id
    ).first()
    
    if draft:
        from app.models.revision import Revision
        revision = Revision(
            draft_id=draft.id,
            section="voice_interview",
            old_text=f"Q: {req.question}\nA: {req.candidate_answer}",
            new_text=f"Score: {result.get('score', 0)}/100\nFeedback: {result.get('feedback', '')}\n\nModel Answer:\n{result.get('model_answer', '')}"
        )
        db.add(revision)
        db.commit()
    
    return {
        "success": True,
        "score": result["score"],
        "feedback": result["feedback"],
        "strengths": result["strengths"],
        "weaknesses": result["weaknesses"],
        "model_answer": result["model_answer"]
    }


@router.post("/start-session")
def start_session(
    req: StartSessionRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Start a new voice interview session - generates the first question.
    """
    application = db.query(Application).filter(
        Application.id == req.application_id,
        Application.user_id == user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if not application.resume_text or not application.job_description:
        raise HTTPException(status_code=400, detail="Application missing resume or job description")
    
    # Generate first question
    result = generate_voice_question(
        resume=application.resume_text,
        jd=application.job_description,
        difficulty=req.difficulty
    )
    
    return {
        "success": True,
        "session_id": f"voice_{application.id}_{user.id}",
        "question": result["question"],
        "type": result["type"],
        "tips": result["tips"],
        "question_number": 1,
        "total_questions": 10,
        "application": {
            "company_name": application.company_name,
            "job_title": application.job_title
        }
    }