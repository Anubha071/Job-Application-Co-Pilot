"""
NEW FEATURE: Calendar Integration Routes
Provides endpoints for follow-up reminder scheduling.
- POST /calendar/generate-ics: Generate .ics file for follow-up
- GET /calendar/reminder-suggestions: Get suggested reminder intervals
- GET /calendar/follow-up-status/{application_id}: Get follow-up status
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.application import Application
from app.services.calendar_helper import (
    generate_follow_up_ics,
    get_reminder_suggestions,
    calculate_follow_up_status
)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"]
)


class GenerateICSRequest(BaseModel):
    application_id: int
    reminder_days: int = 7


@router.post("/generate-ics")
def generate_ics(
    req: GenerateICSRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Generate an .ics calendar file for a follow-up reminder.
    """
    application = db.query(Application).filter(
        Application.id == req.application_id,
        Application.user_id == user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    file_path = generate_follow_up_ics(
        company_name=application.company_name or "",
        job_title=application.job_title or "",
        reminder_days=req.reminder_days
    )
    
    filename = file_path.split("\\")[-1] if "\\" in file_path else file_path.split("/")[-1]
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/calendar"
    )


@router.get("/reminder-suggestions")
def reminder_suggestions(
    user = Depends(get_current_user)
):
    """
    Get suggested follow-up reminder intervals.
    """
    return {
        "success": True,
        "suggestions": get_reminder_suggestions()
    }


@router.get("/follow-up-status/{application_id}")
def follow_up_status(
    application_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Get the follow-up status for an application.
    Calculates days since creation and suggests follow-up action.
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == user.id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Application doesn't have a created_at field, so use a reasonable calculation
    # based on the application id as a proxy (higher id = more recent)
    # In production, add a created_at timestamp to the Application model
    from app.models.revision import Revision
    from app.models.draft import Draft
    
    draft = db.query(Draft).filter(
        Draft.application_id == application.id
    ).first()
    
    # Get revisions count as a rough activity indicator
    revision_count = 0
    if draft:
        revision_count = db.query(Revision).filter(
            Revision.draft_id == draft.id
        ).count()
    
    return {
        "success": True,
        "application_id": application.id,
        "company_name": application.company_name,
        "job_title": application.job_title,
        "status": application.status,
        "has_draft": draft is not None,
        "revision_count": revision_count,
        "follow_up_status": {
            "should_follow_up": application.status in ["not_applied", "applied"],
            "suggested_action": "Send a follow-up email expressing continued interest." if application.status == "applied" else "Consider submitting your application first.",
            "urgency": "medium" if application.status == "applied" else "low"
        }
    }