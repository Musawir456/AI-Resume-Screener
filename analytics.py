"""
analytics.py
Generates analytics charts for the dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def plot_match_scores(results: list) -> go.Figure:
    """Bar chart of candidate match scores."""
    names = [r['resume_name'] for r in results]
    scores = [r['final_match_pct'] for r in results]
    colors = ['#2ecc71' if s >= 40 else '#e74c3c' for s in scores]

    fig = go.Figure(go.Bar(
        x=scores,
        y=names,
        orientation='h',
        marker_color=colors,
        text=[f"{s}%" for s in scores],
        textposition='outside'
    ))
    fig.update_layout(
        title="📊 Candidate Match Scores",
        xaxis_title="Match Percentage (%)",
        yaxis_title="Candidate",
        xaxis=dict(range=[0, 110]),
        height=max(300, len(results) * 50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13)
    )
    return fig


def plot_score_breakdown(result: dict) -> go.Figure:
    """Radar / bar chart of score components for one candidate."""
    categories = ['TF-IDF Score', 'Skill Overlap', 'Keyword Score', 'Final Score']
    values = [
        result['tfidf_score'],
        result['skill_overlap_score'],
        result['keyword_score'],
        result['final_match_pct']
    ]

    fig = go.Figure(go.Bar(
        x=categories,
        y=values,
        marker_color=['#3498db', '#9b59b6', '#f39c12', '#2ecc71'],
        text=[f"{v:.1f}%" for v in values],
        textposition='outside'
    ))
    fig.update_layout(
        title=f"Score Breakdown: {result['resume_name']}",
        yaxis=dict(range=[0, 115], title="Score (%)"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    return fig


def plot_category_distribution(classified_resumes: list) -> go.Figure:
    """Pie chart of resume categories."""
    if not classified_resumes:
        return go.Figure()

    categories = [r.get('predicted_category', 'General') for r in classified_resumes]
    df = pd.DataFrame({'Category': categories})
    counts = df['Category'].value_counts().reset_index()
    counts.columns = ['Category', 'Count']

    fig = px.pie(
        counts, names='Category', values='Count',
        title='📁 Resume Category Distribution',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    return fig


def plot_skill_demand(results: list) -> go.Figure:
    """Bar chart of most demanded skills across all jobs."""
    from collections import Counter
    all_skills = []
    for r in results:
        all_skills.extend(r.get('matched_skills', []))
        all_skills.extend(r.get('missing_skills', []))

    if not all_skills:
        return go.Figure()

    counter = Counter(all_skills)
    top_skills = counter.most_common(10)
    skills, counts = zip(*top_skills)

    fig = go.Figure(go.Bar(
        x=list(skills),
        y=list(counts),
        marker_color='#3498db',
        text=list(counts),
        textposition='outside'
    ))
    fig.update_layout(
        title='🔥 Most In-Demand Skills',
        xaxis_title='Skill',
        yaxis_title='Frequency',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    return fig


def plot_shortlist_pie(results: list) -> go.Figure:
    """Pie chart of shortlisted vs rejected."""
    shortlisted = sum(1 for r in results if '✅' in r['status'])
    rejected = len(results) - shortlisted

    fig = go.Figure(go.Pie(
        labels=['Shortlisted', 'Rejected'],
        values=[shortlisted, rejected],
        marker_colors=['#2ecc71', '#e74c3c'],
        hole=0.4
    ))
    fig.update_layout(
        title='Shortlist Summary',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300
    )
    return fig
