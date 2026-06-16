# 🤖 AI-Based Resume Screening & Job Matching System
**TEYZIX CORE Internship | Task ID: AI-ADV-1**

---

## 📌 Overview
An intelligent resume screening system that automatically matches candidates with job descriptions using NLP and machine learning.

## ⚙️ Features
- **Resume Parsing** — PDF, DOCX, TXT support
- **TF-IDF Matching** — Cosine similarity scoring
- **Skill Overlap** — Keyword-based skill extraction
- **Auto Classification** — IT / Marketing / Finance / Engineering
- **Candidate Ranking** — Sorted by final match %
- **Skill Gap Advisor** — Missing skills + learning resources
- **Analytics Dashboard** — Charts & hiring trends
- **HR AI Chatbot** — Claude-powered assistant

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate sample data (optional)
```bash
python generate_samples.py
```

### 3. Launch the app
```bash
streamlit run app.py
```

## 📁 Project Structure
```
AI-Resume-Screener/
├── app.py                  # Main Streamlit UI
├── resume_parser.py        # PDF/DOCX text extraction
├── job_processor.py        # Job description processing
├── matcher.py              # TF-IDF + skill matching
├── classifier.py           # Resume category classifier
├── analytics.py            # Plotly charts
├── generate_samples.py     # Demo data generator
├── requirements.txt
└── README.md
```

## 📊 Scoring Formula
| Component | Weight |
|-----------|--------|
| TF-IDF Similarity | 40% |
| Skill Overlap | 40% |
| Keyword Match | 20% |

**Shortlist threshold: ≥ 40% final score**

## 🛠️ Tech Stack
- Python, Streamlit, scikit-learn, NLTK
- PyPDF2, python-docx, Plotly, pandas
- Anthropic Claude API (chatbot)

## 📝 Submission
- Task: AI-ADV-1
- Domain: AI / ML / NLP
- Intern: [Your Name]
- LinkedIn: [Your Post Link]
