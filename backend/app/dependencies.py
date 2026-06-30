from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import SECRET_KEY, ALGORITHM
from app.models.user import User

# FIXED: Using HTTPBearer so Swagger UI presents a single bearer token field
# This is the correct scheme for manual Authorization: Bearer <token>
security = HTTPBearer(scheme_name="Bearer")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    
    db: Session = Depends(get_db)
):
    print("=" * 80)
    print("[AUTHORIZATION CHECK STARTED]")
    print(f"Token received: {credentials.credentials[:50]}...")
    print("=" * 80)
    
    token = credentials.credentials
    
    try:
        print(f"DEBUG: Attempting to decode token with SECRET_KEY length: {len(SECRET_KEY)}")
        print(f"DEBUG: Algorithm: {ALGORITHM}")
        
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        
        # BROKEN CODE: No null check for email
        # If payload doesn't have 'sub' key, email will be None
        # and database query will fail silently
        # if email is None:
        #     raise ValueError("Token missing 'sub' claim")
        if email is None:
            raise ValueError("Token missing 'sub' claim")
        
        print(f"[OK] DEBUG: Token decoded successfully")
        
    except Exception as e:
        print(f"[FAIL] DEBUG: Token decode FAILED")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        print(f"   Token length: {len(token)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Invalid token: {str(e)}"
        )
        
    print(f"DEBUG: Looking up user with email: {email}")
    user = db.query(User).filter(
        User.email == email
        ).first()

    if not user:
        print(f"[FAIL] DEBUG: User NOT found in database for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found."
        )
    
    print(f"[OK] DEBUG: User found: {user.email}")
    print("=" * 80)
    return user
