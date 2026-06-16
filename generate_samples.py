"""
generate_samples.py
Creates sample plain-text resumes as .txt files for demo purposes.
Run once: python generate_samples.py
"""

import os

SAMPLE_RESUMES = {
    "Ahmed_Ali_Resume.txt": """Ahmed Ali
ahmed.ali@email.com | +92-300-1234567 | Lahore, Pakistan

OBJECTIVE
Motivated Computer Science graduate seeking a Python Developer role to leverage my NLP and machine learning skills.

EDUCATION
BS Computer Science — FAST NUCES Lahore (2022)
CGPA: 3.5/4.0

SKILLS
Python, Django, Flask, SQL, PostgreSQL, REST APIs, Git, Docker, HTML, CSS, Linux, pandas, numpy, scikit-learn, machine learning

EXPERIENCE
Junior Developer Intern — TechSoft (2022)
- Built REST APIs using Flask and PostgreSQL
- Worked with Python scripts for data processing
- Used Git for version control

PROJECTS
Resume Classifier — Python, sklearn, NLP
- Built a text classifier to categorize resumes into domains

Student Portal — Django, PostgreSQL, HTML/CSS
- Developed full-stack web application for university

CERTIFICATIONS
Python for Data Science — Coursera
Machine Learning Basics — edX
""",

    "Sara_Khan_Resume.txt": """Sara Khan
sara.khan@gmail.com | +92-321-9876543 | Karachi, Pakistan

SUMMARY
Digital Marketing Specialist with 2 years of experience in SEO, SEM, and social media management.

EDUCATION
BBA Marketing — IBA Karachi (2021)

SKILLS
SEO, SEM, Google Ads, Facebook Ads, Social Media Marketing, Content Marketing, Email Marketing, Google Analytics, HubSpot, Copywriting, A/B Testing

EXPERIENCE
Digital Marketing Executive — GrowthAgency (2021-2023)
- Managed SEO campaigns increasing organic traffic by 40%
- Ran Google Ads and Facebook Ads campaigns
- Handled email marketing with Mailchimp

PROJECTS
E-commerce SEO Campaign — Increased sales by 25%
Social Media Strategy for a local brand — grew followers 10x

CERTIFICATIONS
Google Ads Certified
HubSpot Inbound Marketing
""",

    "Usman_Tariq_Resume.txt": """Usman Tariq
usman.tariq@outlook.com | +92-333-5551234 | Islamabad, Pakistan

OBJECTIVE
Data Analyst with strong Python and SQL skills looking for analytical roles.

EDUCATION
BS Statistics — QAU Islamabad (2022)

SKILLS
Python, pandas, numpy, matplotlib, SQL, PostgreSQL, Excel, Tableau, data analysis, machine learning, scikit-learn, NLP, data cleaning, statistical analysis

EXPERIENCE
Data Analyst Trainee — DataLab (2022-2023)
- Performed data cleaning and preprocessing on large datasets
- Built dashboards using Tableau
- Wrote SQL queries for database analysis

PROJECTS
Sales Forecasting Model — Python, sklearn
- Predicted next quarter sales with 85% accuracy

Customer Segmentation — K-Means Clustering
- Clustered 10,000 customers for targeted marketing

CERTIFICATIONS
Data Analysis with Python — IBM
SQL for Data Science — Coursera
""",

    "Zainab_Ahmed_Resume.txt": """Zainab Ahmed
zainab.a@yahoo.com | +92-345-7778899 | Lahore, Pakistan

SUMMARY
Finance graduate with expertise in financial analysis and accounting.

EDUCATION
BBA Finance — LUMS (2021)

SKILLS
Financial Analysis, Excel, Financial Modeling, Accounting, Budgeting, Forecasting, SAP, Financial Reporting, Tax, Risk Management, Balance Sheet, Cash Flow

EXPERIENCE
Junior Financial Analyst — FinancePro (2021-2023)
- Prepared monthly financial reports
- Built financial models for investment analysis
- Assisted in budgeting and forecasting
- Used SAP for ERP operations

CERTIFICATIONS
CFA Level 1 Candidate
Advanced Excel — Microsoft
""",

    "Bilal_Hassan_Resume.txt": """Bilal Hassan
bilal.hassan@gmail.com | +92-311-2223334 | Faisalabad, Pakistan

OBJECTIVE
Machine Learning Engineer passionate about NLP and deep learning.

EDUCATION
MS Artificial Intelligence — UET Lahore (2023)

SKILLS
Python, machine learning, deep learning, NLP, TensorFlow, PyTorch, scikit-learn, pandas, numpy, Docker, AWS, Azure, Git, Linux, SQL, REST APIs, transformers, BERT

EXPERIENCE
ML Research Assistant — UET AI Lab (2021-2023)
- Developed NLP models for Urdu text classification
- Fine-tuned BERT models for sentiment analysis
- Deployed ML models using Docker and AWS

PROJECTS
Urdu Sentiment Analyzer — BERT, PyTorch
- 92% accuracy on Urdu product reviews

Object Detection System — YOLO, TensorFlow
- Real-time detection for surveillance system

CERTIFICATIONS
Deep Learning Specialization — Coursera (Andrew Ng)
AWS Machine Learning Specialty
"""
}


def generate_sample_resumes():
    os.makedirs("data/sample_resumes", exist_ok=True)
    for filename, content in SAMPLE_RESUMES.items():
        path = os.path.join("data/sample_resumes", filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {path}")
    print("\n✅ All sample resumes generated in data/sample_resumes/")


if __name__ == "__main__":
    generate_sample_resumes()
