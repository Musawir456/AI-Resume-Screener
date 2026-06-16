"""
matcher.py
Computes similarity between resumes and job descriptions.
Uses TF-IDF cosine similarity + skill overlap scoring.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from job_processor import ALL_SKILLS, extract_skills_from_job


def compute_tfidf_similarity(resume_text: str, job_text: str) -> float:
    """Compute cosine similarity using TF-IDF vectors."""
    if not resume_text.strip() or not job_text.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score), 4)
    except Exception:
        return 0.0


def compute_skill_overlap(resume_text: str, required_skills: list) -> dict:
    """
    Compute skill overlap between resume and required job skills.
    Returns matched skills, missing skills, and overlap ratio.
    """
    resume_lower = resume_text.lower()
    matched = [s for s in required_skills if s.lower() in resume_lower]
    missing = [s for s in required_skills if s.lower() not in resume_lower]
    overlap = len(matched) / len(required_skills) if required_skills else 0.0
    return {
        'matched_skills': matched,
        'missing_skills': missing,
        'overlap_score': round(overlap, 4)
    }


def compute_keyword_score(resume_text: str, job_text: str) -> float:
    """
    Simple keyword overlap score based on unique important words in job desc.
    """
    from sklearn.feature_extraction.text import CountVectorizer
    try:
        vectorizer = CountVectorizer(stop_words='english', max_features=100)
        vectorizer.fit([job_text])
        job_keywords = set(vectorizer.vocabulary_.keys())
        resume_words = set(resume_text.lower().split())
        if not job_keywords:
            return 0.0
        overlap = job_keywords.intersection(resume_words)
        return round(len(overlap) / len(job_keywords), 4)
    except:
        return 0.0


def compute_final_score(tfidf_score: float, skill_score: float, keyword_score: float) -> float:
    """
    Weighted final match score:
      - TF-IDF similarity: 40%
      - Skill overlap: 40%
      - Keyword overlap: 20%
    """
    final = (tfidf_score * 0.40) + (skill_score * 0.40) + (keyword_score * 0.20)
    return round(final * 100, 2)  # Return as percentage


def match_resume_to_job(resume: dict, job: dict) -> dict:
    """
    Full matching pipeline for one resume against one job.
    Returns all scores and recommendations.
    """
    resume_text = resume.get('clean_text', '')
    job_text = job.get('clean_description', '')
    required_skills = job.get('required_skills', [])

    tfidf = compute_tfidf_similarity(resume_text, job_text)
    skill_data = compute_skill_overlap(resume_text, required_skills)
    keyword = compute_keyword_score(resume_text, job_text)
    final_pct = compute_final_score(tfidf, skill_data['overlap_score'], keyword)

    # Shortlisting threshold
    status = "✅ Shortlisted" if final_pct >= 40 else "❌ Rejected"

    return {
        'resume_name': resume.get('name', 'Unknown'),
        'resume_file': resume.get('filename', ''),
        'job_title': job.get('title', ''),
        'job_id': job.get('id', ''),
        'tfidf_score': round(tfidf * 100, 2),
        'skill_overlap_score': round(skill_data['overlap_score'] * 100, 2),
        'keyword_score': round(keyword * 100, 2),
        'final_match_pct': final_pct,
        'matched_skills': skill_data['matched_skills'],
        'missing_skills': skill_data['missing_skills'],
        'status': status,
        'email': resume.get('email', ''),
        'phone': resume.get('phone', '')
    }


def rank_candidates(resumes: list, job: dict) -> list:
    """
    Match all resumes against a job and return ranked list.
    Sorted by final_match_pct descending.
    """
    results = [match_resume_to_job(r, job) for r in resumes]
    results.sort(key=lambda x: x['final_match_pct'], reverse=True)
    # Add rank
    for i, r in enumerate(results):
        r['rank'] = i + 1
    return results
