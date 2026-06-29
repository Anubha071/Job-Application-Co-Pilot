from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.revision import Revision
import difflib

router = APIRouter(
    prefix="/revisions",
    tags=["Revision"]
)

@router.get(
    "/draft/{draft_id}"
)
def get_revision_history(
    draft_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    
    revisions = db.query(
        Revision
    ).filter(
        Revision.draft_id == draft_id
    ).all()
    
    return revisions

@router.get(
    "/compare/{revision_id}"
)
def compare_revision(

    revision_id: int,

    db: Session = Depends(get_db),

    user=Depends(
        get_current_user
    )
):

    revision = db.query(
        Revision
    ).filter(
        Revision.id == revision_id
    ).first()

    if not revision:

        raise HTTPException(
            status_code=404,
            detail="Revision not found"
        )

    diff = list(

        difflib.ndiff(

            revision.old_text.splitlines(),

            revision.new_text.splitlines()
        )
    )

    return {

        "revision_id":
        revision.id,

        "old_text":
        revision.old_text,

        "new_text":
        revision.new_text,

        "diff":
        diff
    }
    