"""
classifier.py
Classifies resumes into domain categories using keyword scoring.
Categories: IT, Marketing, Finance, Engineering
"""

from job_processor import SKILL_KEYWORDS


def classify_resume(resume_text: str) -> dict:
    """
    Classify resume into a domain category based on keyword density.
    Returns predicted category and confidence scores per category.
    """
    text_lower = resume_text.lower()
    scores = {}

    for category, keywords in SKILL_KEYWORDS.items():
        matched = [kw for kw in keywords if kw.lower() in text_lower]
        scores[category] = len(matched)

    total = sum(scores.values())
    if total == 0:
        return {
            'predicted_category': 'General',
            'confidence_scores': {k: 0.0 for k in SKILL_KEYWORDS},
            'matched_per_category': scores
        }

    confidence = {k: round(v / total * 100, 1) for k, v in scores.items()}
    predicted = max(scores, key=scores.get)

    return {
        'predicted_category': predicted,
        'confidence_scores': confidence,
        'matched_per_category': scores
    }


def get_skill_gap_recommendations(matched_skills: list, missing_skills: list, category: str) -> dict:
    """
    Generate skill gap analysis and improvement recommendations.
    """
    recommendations = []
    learning_resources = {
        'python': 'Learn Python: https://www.python.org/doc/',
        'machine learning': 'ML Course: Coursera / Andrew Ng',
        'sql': 'SQL Tutorial: https://www.w3schools.com/sql/',
        'react': 'React Docs: https://react.dev/',
        'docker': 'Docker Docs: https://docs.docker.com/',
        'aws': 'AWS Free Tier: https://aws.amazon.com/free/',
        'seo': 'Google SEO Guide: https://developers.google.com/search',
        'excel': 'Excel Skills: Microsoft Learn',
        'financial modeling': 'CFI Financial Modeling: https://corporatefinanceinstitute.com/',
    }

    for skill in missing_skills[:5]:  # Top 5 missing skills
        resource = learning_resources.get(skill.lower(), f'Search: "{skill} tutorial"')
        recommendations.append({
            'skill': skill,
            'resource': resource
        })

    strength_level = "Strong" if len(matched_skills) > 5 else \
                     "Moderate" if len(matched_skills) > 2 else "Needs Improvement"

    return {
        'strength_level': strength_level,
        'matched_count': len(matched_skills),
        'missing_count': len(missing_skills),
        'top_recommendations': recommendations,
        'summary': f"You match {len(matched_skills)} required skills. "
                   f"Focus on learning: {', '.join(missing_skills[:3]) if missing_skills else 'All key skills covered!'}"
    }
