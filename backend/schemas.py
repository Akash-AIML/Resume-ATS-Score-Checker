from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleAuthRequest(BaseModel):
    token: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Job Schemas
class JobSectionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    display_order: int
    
    class Config:
        from_attributes = True

class JobRoleCreate(BaseModel):
    section_id: int
    title: str
    description: str
    requirements: str

class JobRoleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None

class JobRoleResponse(BaseModel):
    id: int
    section_id: int
    title: str
    description: str
    requirements: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class JobDocumentResponse(BaseModel):
    id: int
    job_id: int
    filename: str
    file_type: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Resume Schemas
class ResumeUploadResponse(BaseModel):
    id: int
    filename: str
    job_id: int
    upload_date: datetime
    
    class Config:
        from_attributes = True

# Ranking Schemas
class RankingRequest(BaseModel):
    job_id: int

class RankingResultResponse(BaseModel):
    id: int
    job_id: int
    resume_id: int
    score: float
    breakdown: Dict[str, float]
    ranked_at: datetime
    
    class Config:
        from_attributes = True

class ExplanationResponse(BaseModel):
    overall_assessment: str
    matched_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    improvement_suggestions: List[str]
    score: float
    breakdown: Dict[str, float]
