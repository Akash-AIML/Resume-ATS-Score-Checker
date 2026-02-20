from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for Google OAuth
    role = Column(String, nullable=False, default="user")  # admin or user
    google_id = Column(String, unique=True, nullable=True)  # For Google OAuth
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resumes = relationship("Resume", back_populates="user")

class JobSection(Base):
    __tablename__ = "job_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String)
    display_order = Column(Integer, nullable=False)
    
    job_roles = relationship("JobRole", back_populates="section")

class JobRole(Base):
    __tablename__ = "job_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("job_sections.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    section = relationship("JobSection", back_populates="job_roles")
    documents = relationship("JobDocument", back_populates="job")
    resumes = relationship("Resume", back_populates="job")
    ranking_results = relationship("RankingResult", back_populates="job")

class JobDocument(Base):
    __tablename__ = "job_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_roles.id", ondelete="CASCADE"))
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    job = relationship("JobRole", back_populates="documents")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("job_roles.id"))
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="resumes")
    job = relationship("JobRole", back_populates="resumes")
    ranking_results = relationship("RankingResult", back_populates="resume")

class RankingResult(Base):
    __tablename__ = "ranking_results"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_roles.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    score = Column(Float, nullable=False)
    breakdown = Column(JSON, nullable=False)  # {skills, experience, education, projects}
    explanation = Column(Text)
    ranked_at = Column(DateTime, default=datetime.utcnow)
    
    job = relationship("JobRole", back_populates="ranking_results")
    resume = relationship("Resume", back_populates="ranking_results")
