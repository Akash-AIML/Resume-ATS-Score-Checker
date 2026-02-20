'use client';

import { useState, useRef } from 'react';
import { Upload, FileText, Sparkles, TrendingUp, CheckCircle, AlertCircle, Loader2, FileUp } from 'lucide-react';
import apiClient from '@/lib/api';

interface AnalysisResult {
    score: number;
    breakdown: {
        skills: number;
        experience: number;
        education: number;
        projects: number;
    };
    overall_assessment: string;
    matched_skills: string[];
    missing_skills: string[];
    strengths: string[];
    improvement_suggestions: string[];
}

export default function HomePage() {
    const [resumeFile, setResumeFile] = useState<File | null>(null);
    const [jobDescriptionText, setJobDescriptionText] = useState('');
    const [jobDescriptionFile, setJobDescriptionFile] = useState<File | null>(null);
    const [useTextInput, setUseTextInput] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState<AnalysisResult | null>(null);
    
    const resumeInputRef = useRef<HTMLInputElement>(null);
    const jobInputRef = useRef<HTMLInputElement>(null);

    const handleResumeUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            if (!file.name.toLowerCase().endsWith('.pdf')) {
                setError('Please upload a PDF file');
                return;
            }
            setResumeFile(file);
            setError('');
        }
    };

    const handleJobFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            if (!file.name.toLowerCase().endsWith('.pdf')) {
                setError('Please upload a PDF file');
                return;
            }
            setJobDescriptionFile(file);
            setError('');
        }
    };

    const handleAnalyze = async () => {
        if (!resumeFile) {
            setError('Please upload your resume');
            return;
        }

        if (useTextInput && !jobDescriptionText.trim()) {
            setError('Please enter a job description');
            return;
        }

        if (!useTextInput && !jobDescriptionFile) {
            setError('Please upload a job description PDF');
            return;
        }

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const formData = new FormData();
            formData.append('resume', resumeFile);
            
            if (useTextInput) {
                formData.append('job_description_text', jobDescriptionText);
            } else if (jobDescriptionFile) {
                formData.append('job_description_file', jobDescriptionFile);
            }

            const response = await apiClient.post<AnalysisResult>('/analyze/resume', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setResult(response.data);
        } catch (err: any) {
            console.error('Analysis error:', err);
            setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score: number) => {
        if (score >= 80) return 'text-green-600';
        if (score >= 60) return 'text-yellow-600';
        return 'text-red-600';
    };

    const getScoreBgColor = (score: number) => {
        if (score >= 80) return 'from-green-500 to-green-600';
        if (score >= 60) return 'from-yellow-500 to-yellow-600';
        return 'from-red-500 to-red-600';
    };

    return (
        <div className="min-h-screen py-8 px-4">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12 animate-fade-in">
                    <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                        <Sparkles className="w-10 h-10 text-white" />
                    </div>
                    <h1 className="text-5xl font-bold mb-4">
                        <span className="text-gradient">Resume Score Analyzer</span>
                    </h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Upload your resume and job description to get an AI-powered score 
                        and personalized suggestions to improve your chances.
                    </p>
                </div>

                {/* Main Form */}
                <div className="glass-card rounded-2xl p-8 mb-8">
                    <div className="space-y-8">
                        {/* Resume Upload */}
                        <div>
                            <label className="block text-lg font-semibold text-gray-800 mb-3">
                                <FileText className="w-5 h-5 inline-block mr-2" />
                                Upload Your Resume (PDF)
                            </label>
                            <div 
                                onClick={() => resumeInputRef.current?.click()}
                                className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
                                    resumeFile 
                                        ? 'border-green-400 bg-green-50' 
                                        : 'border-gray-300 hover:border-primary-400 hover:bg-primary-50'
                                }`}
                            >
                                <input
                                    ref={resumeInputRef}
                                    type="file"
                                    accept=".pdf"
                                    onChange={handleResumeUpload}
                                    className="hidden"
                                />
                                {resumeFile ? (
                                    <div className="flex items-center justify-center gap-3">
                                        <CheckCircle className="w-8 h-8 text-green-500" />
                                        <span className="text-lg font-medium text-green-700">{resumeFile.name}</span>
                                    </div>
                                ) : (
                                    <div>
                                        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                                        <p className="text-gray-600">Click to upload or drag and drop</p>
                                        <p className="text-sm text-gray-400 mt-1">PDF files only</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Job Description Input */}
                        <div>
                            <label className="block text-lg font-semibold text-gray-800 mb-3">
                                <FileUp className="w-5 h-5 inline-block mr-2" />
                                Job Description
                            </label>
                            
                            {/* Toggle */}
                            <div className="flex gap-4 mb-4">
                                <button
                                    onClick={() => setUseTextInput(true)}
                                    className={`px-4 py-2 rounded-lg font-medium transition-all ${
                                        useTextInput 
                                            ? 'bg-primary-600 text-white' 
                                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                    }`}
                                >
                                    Paste Text
                                </button>
                                <button
                                    onClick={() => setUseTextInput(false)}
                                    className={`px-4 py-2 rounded-lg font-medium transition-all ${
                                        !useTextInput 
                                            ? 'bg-primary-600 text-white' 
                                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                    }`}
                                >
                                    Upload PDF
                                </button>
                            </div>

                            {useTextInput ? (
                                <textarea
                                    value={jobDescriptionText}
                                    onChange={(e) => setJobDescriptionText(e.target.value)}
                                    placeholder="Paste the job description here..."
                                    className="input-field min-h-[200px] resize-y"
                                    rows={8}
                                />
                            ) : (
                                <div 
                                    onClick={() => jobInputRef.current?.click()}
                                    className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
                                        jobDescriptionFile 
                                            ? 'border-green-400 bg-green-50' 
                                            : 'border-gray-300 hover:border-primary-400 hover:bg-primary-50'
                                    }`}
                                >
                                    <input
                                        ref={jobInputRef}
                                        type="file"
                                        accept=".pdf"
                                        onChange={handleJobFileUpload}
                                        className="hidden"
                                    />
                                    {jobDescriptionFile ? (
                                        <div className="flex items-center justify-center gap-3">
                                            <CheckCircle className="w-8 h-8 text-green-500" />
                                            <span className="text-lg font-medium text-green-700">{jobDescriptionFile.name}</span>
                                        </div>
                                    ) : (
                                        <div>
                                            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                                            <p className="text-gray-600">Click to upload job description PDF</p>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>

                        {/* Error Message */}
                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
                                <AlertCircle className="w-5 h-5" />
                                {error}
                            </div>
                        )}

                        {/* Analyze Button */}
                        <button
                            onClick={handleAnalyze}
                            disabled={loading}
                            className="w-full btn-primary text-lg py-4 flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-6 h-6 animate-spin" />
                                    Analyzing...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-6 h-6" />
                                    Analyze Resume
                                </>
                            )}
                        </button>
                    </div>
                </div>

                {/* Results */}
                {result && (
                    <div className="space-y-6 animate-slide-up">
                        {/* Score Card */}
                        <div className="glass-card rounded-2xl p-8">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-2xl font-bold text-gray-800">Your Resume Score</h2>
                                <div className={`text-5xl font-bold bg-gradient-to-r ${getScoreBgColor(result.score)} bg-clip-text text-transparent`}>
                                    {result.score.toFixed(0)}%
                                </div>
                            </div>

                            {/* Score Breakdown */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {Object.entries(result.breakdown).map(([key, value]) => (
                                    <div key={key} className="bg-gray-50 rounded-xl p-4 text-center">
                                        <p className="text-sm text-gray-500 capitalize mb-1">{key}</p>
                                        <p className={`text-2xl font-bold ${getScoreColor(value)}`}>
                                            {value.toFixed(0)}%
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Overall Assessment */}
                        <div className="glass-card rounded-2xl p-8">
                            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                <TrendingUp className="w-6 h-6 text-primary-600" />
                                Overall Assessment
                            </h3>
                            <p className="text-gray-700 leading-relaxed">{result.overall_assessment}</p>
                        </div>

                        {/* Skills Analysis */}
                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Matched Skills */}
                            <div className="glass-card rounded-2xl p-6">
                                <h3 className="text-lg font-bold text-green-700 mb-4 flex items-center gap-2">
                                    <CheckCircle className="w-5 h-5" />
                                    Matched Skills
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {result.matched_skills.length > 0 ? (
                                        result.matched_skills.map((skill, i) => (
                                            <span key={i} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                                                {skill}
                                            </span>
                                        ))
                                    ) : (
                                        <p className="text-gray-500">No specific matches found</p>
                                    )}
                                </div>
                            </div>

                            {/* Missing Skills */}
                            <div className="glass-card rounded-2xl p-6">
                                <h3 className="text-lg font-bold text-red-700 mb-4 flex items-center gap-2">
                                    <AlertCircle className="w-5 h-5" />
                                    Missing Skills
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {result.missing_skills.length > 0 ? (
                                        result.missing_skills.map((skill, i) => (
                                            <span key={i} className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-medium">
                                                {skill}
                                            </span>
                                        ))
                                    ) : (
                                        <p className="text-gray-500">No critical gaps found</p>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Strengths */}
                        {result.strengths.length > 0 && (
                            <div className="glass-card rounded-2xl p-6">
                                <h3 className="text-lg font-bold text-gray-800 mb-4">Your Strengths</h3>
                                <ul className="space-y-2">
                                    {result.strengths.map((strength, i) => (
                                        <li key={i} className="flex items-start gap-2">
                                            <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                                            <span className="text-gray-700">{strength}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Improvement Suggestions */}
                        {result.improvement_suggestions.length > 0 && (
                            <div className="glass-card rounded-2xl p-6 border-2 border-primary-200">
                                <h3 className="text-xl font-bold text-primary-700 mb-4 flex items-center gap-2">
                                    <Sparkles className="w-6 h-6" />
                                    How to Improve Your Resume
                                </h3>
                                <ul className="space-y-3">
                                    {result.improvement_suggestions.map((suggestion, i) => (
                                        <li key={i} className="flex items-start gap-3 bg-primary-50 rounded-lg p-3">
                                            <span className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0">
                                                {i + 1}
                                            </span>
                                            <span className="text-gray-700">{suggestion}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Try Again Button */}
                        <div className="text-center">
                            <button
                                onClick={() => {
                                    setResult(null);
                                    setResumeFile(null);
                                    setJobDescriptionText('');
                                    setJobDescriptionFile(null);
                                }}
                                className="btn-secondary"
                            >
                                Analyze Another Resume
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}