export interface User {
    id: number;
    email: string;
    role: 'admin' | 'user';
}

export interface JobSection {
    id: number;
    name: string;
    description: string;
    icon: string;
    display_order: number;
}

export interface JobRole {
    id: number;
    section_id: number;
    title: string;
    description: string;
    requirements: string;
    created_at: string;
    updated_at: string;
}

export interface JobDocument {
    id: number;
    job_id: number;
    filename: string;
    file_type: string;
    s3_url: string;
    uploaded_at: string;
}

export interface Resume {
    id: number;
    user_id: number;
    job_id: number;
    filename: string;
    s3_url: string;
    upload_date: string;
}

export interface RankingResult {
    id: number;
    job_id: number;
    resume_id: number;
    score: number;
    breakdown: {
        skills: number;
        experience: number;
        education: number;
        projects: number;
    };
    explanation?: string;
    ranked_at: string;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
    user: User;
}

export interface RegisterRequest {
    email: string;
    password: string;
    role?: 'admin' | 'user';
}
