"""
job_processor.py
Processes job descriptions and extracts required skills/keywords.
"""

import re
import json

# Master skill list across domains
SKILL_KEYWORDS = {
    'IT': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'sql', 'nosql',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'linux',
        'machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch',
        'scikit-learn', 'pandas', 'numpy', 'data analysis', 'api', 'rest',
        'mongodb', 'postgresql', 'mysql', 'redis', 'microservices', 'devops',
        'html', 'css', 'bootstrap', 'tailwind', 'agile', 'scrum'
    ],
    'Marketing': [
        'seo', 'sem', 'google ads', 'facebook ads', 'social media', 'content marketing',
        'email marketing', 'brand management', 'market research', 'crm',
        'google analytics', 'hubspot', 'salesforce', 'copywriting', 'pr',
        'digital marketing', 'influencer marketing', 'affiliate marketing',
        'a/b testing', 'conversion rate', 'lead generation', 'marketing strategy'
    ],
    'Finance': [
        'accounting', 'financial analysis', 'excel', 'financial modeling',
        'quickbooks', 'sap', 'erp', 'tax', 'audit', 'budgeting', 'forecasting',
        'investment', 'portfolio management', 'risk management', 'financial reporting',
        'balance sheet', 'cash flow', 'valuation', 'bloomberg', 'cfa', 'cpa'
    ],
    'Engineering': [
        'autocad', 'solidworks', 'matlab', 'simulation', 'circuit design',
        'pcb', 'embedded systems', 'plc', 'scada', 'pid control',
        'mechanical design', 'thermodynamics', 'structural analysis', 'catia',
        'ansys', 'project management', 'quality control', 'six sigma', 'lean'
    ]
}

# Flatten all skills into one list
ALL_SKILLS = list(set(
    skill for skills in SKILL_KEYWORDS.values() for skill in skills
))

# Sample job descriptions for demo
SAMPLE_JOBS = [
    {
        "id": "JD001",
        "title": "Junior Python Developer",
        "company": "TechCorp",
        "category": "IT",
        "description": """
        We are looking for a Junior Python Developer to join our team.
        Requirements:
        - Proficiency in Python and Django or Flask
        - Experience with SQL and PostgreSQL databases
        - Knowledge of REST APIs and JSON
        - Familiarity with Git version control
        - Understanding of HTML, CSS basics
        - Experience with Docker is a plus
        - Good problem-solving skills
        - Team player with good communication skills
        Responsibilities:
        - Develop and maintain backend services
        - Write clean, testable code
        - Participate in code reviews
        - Collaborate with frontend developers
        """
    },
    {
        "id": "JD002",
        "title": "Data Analyst",
        "company": "DataVision",
        "category": "IT",
        "description": """
        Seeking a Data Analyst with strong analytical skills.
        Requirements:
        - Strong Python skills (pandas, numpy, matplotlib)
        - SQL and database querying
        - Data visualization (Tableau or Power BI)
        - Machine learning basics (scikit-learn)
        - Excel advanced functions
        - Statistical analysis knowledge
        - Experience with data cleaning and preprocessing
        - NLP basics a plus
        """
    },
    {
        "id": "JD003",
        "title": "Digital Marketing Specialist",
        "company": "GrowthHub",
        "category": "Marketing",
        "description": """
        Looking for a Digital Marketing Specialist.
        Requirements:
        - SEO and SEM expertise
        - Google Ads and Facebook Ads experience
        - Social media management
        - Content marketing and copywriting
        - Google Analytics proficiency
        - Email marketing (Mailchimp or HubSpot)
        - A/B testing experience
        - Strong analytical skills
        """
    },
    {
        "id": "JD004",
        "title": "Financial Analyst",
        "company": "FinanceGroup",
        "category": "Finance",
        "description": """
        We need a Financial Analyst with 1-2 years experience.
        Requirements:
        - Financial modeling and analysis
        - Advanced Excel skills
        - Accounting principles knowledge
        - Budgeting and forecasting
        - Financial reporting
        - SAP or ERP experience preferred
        - CFA or CPA certification a plus
        - Strong attention to detail
        """
    },
    {
        "id": "JD005",
        "title": "Machine Learning Engineer",
        "company": "AI Solutions",
        "category": "IT",
        "description": """
        Exciting opportunity for an ML Engineer.
        Requirements:
        - Strong Python programming
        - Machine learning algorithms (sklearn, TensorFlow, PyTorch)
        - NLP and text processing
        - Deep learning experience
        - Data preprocessing and feature engineering
        - Model deployment experience
        - Docker and cloud (AWS/Azure) knowledge
        - Git and version control
        - Strong mathematics and statistics
        """
    }
]


def clean_job_text(text: str) -> str:
    """Clean job description text."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s\+\#\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_skills_from_job(job_text: str) -> list:
    """Extract skill keywords present in job description."""
    job_lower = job_text.lower()
    found = []
    for skill in ALL_SKILLS:
        if skill.lower() in job_lower:
            found.append(skill)
    return found


def process_job(job: dict) -> dict:
    """Process a single job description dict."""
    clean_desc = clean_job_text(job['description'])
    skills = extract_skills_from_job(job['description'])
    return {
        **job,
        'clean_description': clean_desc,
        'required_skills': skills,
        'skill_count': len(skills)
    }


def get_all_jobs() -> list:
    """Return all processed sample jobs."""
    return [process_job(j) for j in SAMPLE_JOBS]


def get_job_by_id(job_id: str) -> dict:
    """Fetch a specific job by ID."""
    for job in SAMPLE_JOBS:
        if job['id'] == job_id:
            return process_job(job)
    return None
