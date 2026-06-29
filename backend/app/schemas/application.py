from pydantic import BaseModel

# Schemas for application management

class ApplicationCreate(BaseModel):
    company_name : str
    job_title : str
    status : str
    notes : str | None = None # Optional field for additional notes about the application.
    
class ApplicationResponse(BaseModel):
    id : int
    company_name : str
    job_title : str
    status : str
    resume_filename = str
    notes : str | None = None
    
    class Config:
        form_attribute = True
        