from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, Token
from app.utils.auth import verify_password, create_access_token, hash_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

DEMO_EMAIL = "demo@jobcopilot.app"
DEMO_PASSWORD = "demo123"
DEMO_USERNAME = "Demo User"

@router.post("/auto-login", response_model=Token)
def auto_login(db: Session = Depends(get_db)):
    """Auto-login with a demo account. Creates the demo user if it doesn't exist."""
    demo_user = db.query(User).filter(User.email == DEMO_EMAIL).first()
    
    if not demo_user:
        hashed = hash_password(DEMO_PASSWORD)
        demo_user = User(email=DEMO_EMAIL, username=DEMO_USERNAME, password=hashed)
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
    
    access_token = create_access_token(data={"sub": demo_user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Hash the password and create a new user
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User registered successfully",
    }

@router.post("/login", response_model=Token)
def login(
    user: UserLogin, 
    db: Session = Depends(get_db)
):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    # Create a JWT token for the authenticated user
    access_token = create_access_token(data={"sub": db_user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }