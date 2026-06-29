from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# This file contains utility functions for authentication, including password hashing and JWT token creation and verification.

pwd = CryptContext(
    schemes=["argon2"], # We are using argon2 for hashing passwords.
    deprecated="auto" # This will automatically mark any old hashing schemes as deprecated.
)

def hash_password(password: str) -> str:
    #  bcrypt pnly supports upto 72 bytes
    safe_password = password[:72]
    return pwd.hash(safe_password) # This function hashes the provided password.

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd.verify(plain_password[:72], hashed_password) # This function verifies that the provided plain password matches the hashed password.

def create_access_token(data):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    payload["exp"] = expire # This adds an expiration time to the token.
    
    return jwt.encode(
        payload, 
        SECRET_KEY,
        algorithm = ALGORITHM
    )