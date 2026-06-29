from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.draft import Draft
from app.services.doc_generator import create_cover_letter_docx, create_resume_docx
from app.services.pdf_generator import create_resume_pdf

router = APIRouter(
    prefix = "/downloads",
    tags = ["Downloads"]
)

@router.get("/cover-docx/{draft_id}")

def download_cover_docx(
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
        raise HTTPException(404, "Draft not Found")
    
    file_path = create_cover_letter_docx(
        f"cover_letter_{draft_id}.docx",
        draft.cover_letter
    )
    
    return FileResponse(
        path = file_path, 
        filename= f"cover_letter_{draft_id}.docx"
    )
    
@router.get("/resume-docx/{draft_id}")
def download_resume_docx(
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
        raise HTTPException(404, "Draft not Found")
    
    file_path = create_resume_docx(f"resume_{draft_id}.docx", draft.resume_rewrite)
    
    return FileResponse(
        path= file_path,
        filename=f"resume_{draft.id}.docx"
    )
    
@router.get("/resume-pdf/{draft_id}")
def download_resume_pdf(
    draft_id: int,
    db: Session= Depends(get_db),
    user=Depends(get_current_user)
):
    
    draft = db.query(
        Draft
    ).filter(
        Draft.id == draft_id
    ).first()
    
    # BROKEN CODE: capital F prefix is invalid Python syntax
    file_path = create_resume_pdf(
        f"resume_{draft_id}.pdf",
        draft.resume_rewrite
    )
    return FileResponse(
        path = file_path,
        filename= f"resume_{draft.id}.pdf"
    )