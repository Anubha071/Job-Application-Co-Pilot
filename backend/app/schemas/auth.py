from pydantic import BaseModel, EmailStr, constr

# Schemas for user authentication and registration

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password : constr(max_length=72)
    
class UserLogin(BaseModel):
    email : EmailStr
    password : constr(max_length=72)
    
class UserResponse(BaseModel):
    id : int
    email : EmailStr
    username : str
        
    class Config:
        from_attributes = True # This allows Pydantic to work with SQLAlchemy models.

class Token(BaseModel):
    access_token : str
    token_type : str
        