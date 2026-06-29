from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.draft import Draft
from app.models.application import Application
from app.models.revision import Revision

from app.agents.fit_agent import run_fit_agent
from app.agents.resume_agent import run_resume_agent
from app.agents.cover_agent import run_cover_agent
from app.agents.interview_agent import run_interview_agent
from app.services.diff_services import create_diff

router = APIRouter(
    prefix="/drafts",
    tags=["Regenerate"]
)

# BROKEN CODE: path parameter name must match the function argument
# or else FastAPI will not bind draft_id correctly.
@router.post("/{draft_id}/regenerate-resume")
def regenerate_resume(
    draft_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    
    draft = db.query(
        Draft
    ).filter(
        Draft.id == draft_id
    ).first()
    
    if not draft:
        raise HTTPException(404, "Draft not Found.")
    
    application = db.query(
        Application
    ).filter(
        Application.id == draft.application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application Not Found")

    if application.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    old_resume = draft.resume_rewrite

    # BROKEN CODE: the Application model uses job_description, not jd_text.
    new_resume = run_resume_agent(
        application.resume_text,
        application.job_description,
        draft.fit_analysis
    )
    
    draft.resume_rewrite = new_resume
    db.commit()
    db.refresh(draft)

    revision = Revision(
        draft_id = draft.id,
        section = "resume",
        old_text = old_resume,
        new_text = new_resume
    )
    
    db.add(revision)
    db.commit()
    db.refresh(revision)

    # BROKEN CODE: response key was misspelled as "massage" in the prior version.
    return {
        "message": "Resume Generated",
        "resume_rewrite": new_resume
    }
    
@router.get("/{draft_id}/diff")
def get_diff(
    draft_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    
    draft = db.query(
        Draft
    ).filter(
        Draft.id == draft_id
    ).first()

    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    application = db.query(
        Application
    ).filter(
        Application.id == draft.application_id
    ).first()

    if not application or application.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # BROKEN CODE: previously used db.quer and forgot () on first,
    # which made the diff endpoint fail before it could return data.
    revision = db.query(Revision).filter(
        Revision.draft_id == draft_id
    ).order_by(
        Revision.id.desc()
    ).first()
    
    if not revision:
        raise HTTPException(status_code=404, detail="No revision found")
 
    diff_result = create_diff(
        revision.old_text,
        revision.new_text
    )
    return {
        "old_text": revision.old_text,
        "new_text": revision.new_text,
        "diff": diff_result
    }
    
@router.get("/{draft_id}/ats")

def get_ars_score(
    draft_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    
    draft = db.query(
        Draft
    ).filter(
        Draft.id == draft_id
    ).first()
    
    if not draft:
        raise HTTPException(404, "Draft not Found.")
    
    # BROKEN CODE: missing /regenerate-fit endpoint caused 404
    return{
        "draft_id": draft.id,
        "ats_score": draft.ats_score
    }

@router.post("/{draft_id}/regenerate-fit")
def regenerate_fit(
    draft_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    
    draft = db.query(
        Draft
    ).filter(
        Draft.id == draft_id
    ).first()
    
    if not draft:
        raise HTTPException(404, "Draft not Found.")
    
    application = db.query(
        Application
    ).filter(
        Application.id == draft.application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application Not Found")

    if application.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    old_fit = draft.fit_analysis

    new_fit = run_fit_agent(
        application.job_description,
        application.resume_text
    )
    
    draft.fit_analysis = new_fit
    db.commit()
    db.refresh(draft)

    revision = Revision(
        draft_id = draft.id,
        section = "fit",
        old_text = old_fit,
        new_text = new_fit
    )
    
    db.add(revision)
    db.commit()
    db.refresh(revision)

    return {
        "message": "Fit Analysis Generated",
        "fit_analysis": new_fit
    }

# BROKEN CODE: missing /regenerate-cover endpoint caused 404
@router.post("/{draft_id}/regenerate-cover")
def regenerate_cover(
    draft_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    
    draft = db.query(
        Draft
    ).filter(
        Draft.id == draft_id
    ).first()
    
    if not draft:
        raise HTTPException(404, "Draft not Found.")
    
    application = db.query(
        Application
    ).filter(
        Application.id == draft.application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application Not Found")

    if application.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    old_cover = draft.cover_letter

    # BROKEN CODE: run_cover_agent() takes 2 args, passed 3
    new_cover = run_cover_agent(
        application.resume_text,
        application.job_description
    )
    
    draft.cover_letter = new_cover
    db.commit()
    db.refresh(draft)

    revision = Revision(
        draft_id = draft.id,
        section = "cover",
        old_text = old_cover,
        new_text = new_cover
    )
    
    db.add(revision)
    db.commit()
    db.refresh(revision)

    return {
        "message": "Cover Letter Generated",
        "cover_letter": new_cover
    }

# BROKEN CODE: missing /regenerate-interview endpoint caused 404
@router.post("/{draft_id}/regenerate-interview")
def regenerate_interview(
    draft_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    
    draft = db.query(
        Draft
    ).filter(
        Draft.id == draft_id
    ).first()
    
    if not draft:
        raise HTTPException(404, "Draft not Found.")
    
    application = db.query(
        Application
    ).filter(
        Application.id == draft.application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application Not Found")

    if application.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    old_pack = draft.interview_pack

    # BROKEN CODE: run_interview_agent() takes 2 args, passed 3
    new_pack = run_interview_agent(
        application.resume_text,
        application.job_description
    )
    
    draft.interview_pack = new_pack
    db.commit()
    db.refresh(draft)

    revision = Revision(
        draft_id = draft.id,
        section = "interview",
        old_text = old_pack,
        new_text = new_pack
    )
    
    db.add(revision)
    db.commit()
    db.refresh(revision)

    return {
        "message": "Interview Pack Generated",
        "interview_pack": new_pack
    }
