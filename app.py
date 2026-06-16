"""
app.py — AI-Based Resume Screening & Job Matching System
TEYZIX CORE Internship | Task ID: AI-ADV-1
"""

import streamlit as st
import pandas as pd
import os
import sys

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Screener | TEYZIX",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0f1117; }

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1e2130, #252840);
    border: 1px solid #2d3250;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin-bottom: 12px;
}
.metric-number { font-size: 2.2rem; font-weight: 700; color: #00d4aa; }
.metric-label  { font-size: 0.85rem; color: #8892b0; margin-top: 4px; }

/* Score badge */
.score-high   { color: #00d4aa; font-weight: 700; font-size: 1.4rem; }
.score-medium { color: #f39c12; font-weight: 700; font-size: 1.4rem; }
.score-low    { color: #e74c3c; font-weight: 700; font-size: 1.4rem; }

/* Status badges */
.badge-green {
    background: #0d3b2e; color: #00d4aa;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600;
    border: 1px solid #00d4aa44;
}
.badge-red {
    background: #3b0d0d; color: #e74c3c;
    padding: 3px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600;
    border: 1px solid #e74c3c44;
}

/* Section headers */
.section-title {
    font-size: 1.1rem; font-weight: 600;
    color: #ccd6f6; margin-bottom: 8px;
    border-left: 3px solid #00d4aa;
    padding-left: 10px;
}

/* Skill pill */
.skill-pill {
    display: inline-block;
    background: #1a2744; color: #64b5f6;
    border: 1px solid #1e3a5f;
    border-radius: 20px; padding: 2px 10px;
    font-size: 0.75rem; margin: 2px;
}
.skill-pill-miss {
    display: inline-block;
    background: #2a1a1a; color: #ef9a9a;
    border: 1px solid #5f1e1e;
    border-radius: 20px; padding: 2px 10px;
    font-size: 0.75rem; margin: 2px;
}

/* Rank badge */
.rank-1 { color: #FFD700; font-size: 1.3rem; }
.rank-2 { color: #C0C0C0; font-size: 1.3rem; }
.rank-3 { color: #CD7F32; font-size: 1.3rem; }

/* Progress bar container */
.prog-bar-bg {
    background: #1e2130; border-radius: 8px;
    height: 10px; margin: 6px 0;
}
.prog-bar-fill {
    height: 10px; border-radius: 8px;
    background: linear-gradient(90deg, #00d4aa, #0080ff);
}

/* Upload zone style override */
[data-testid="stFileUploader"] {
    background: #1e2130 !important;
    border: 2px dashed #2d3250 !important;
    border-radius: 12px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161824 !important;
}
</style>
""", unsafe_allow_html=True)

# ── imports (with install fallback) ──────────────────────────────────────────
try:
    from resume_parser import parse_resume, clean_text
    from job_processor import get_all_jobs, get_job_by_id, extract_skills_from_job
    from matcher import rank_candidates, match_resume_to_job
    from classifier import classify_resume, get_skill_gap_recommendations
    from analytics import (plot_match_scores, plot_score_breakdown,
                            plot_category_distribution, plot_skill_demand,
                            plot_shortlist_pie)
except ModuleNotFoundError as e:
    st.error(f"Module not found: {e}. Make sure all .py files are in the same folder.")
    st.stop()

# ── session state ─────────────────────────────────────────────────────────────
if 'parsed_resumes'  not in st.session_state: st.session_state.parsed_resumes  = []
if 'match_results'   not in st.session_state: st.session_state.match_results   = []
if 'selected_job_id' not in st.session_state: st.session_state.selected_job_id = None
if 'classified'      not in st.session_state: st.session_state.classified      = []

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size:2rem;'>🤖</div>
        <div style='font-size:1.1rem; font-weight:700; color:#00d4aa;'>AI Resume Screener</div>
        <div style='font-size:0.75rem; color:#8892b0; margin-top:4px;'>TEYZIX CORE · AI-ADV-1</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠 Dashboard",
        "📤 Upload Resumes",
        "🎯 Match & Rank",
        "📊 Analytics",
        "💡 Skill Advisor",
        "🧠 HR Chatbot"
    ])

    st.markdown("---")

    # Load sample data button
    if st.button("🔄 Load Demo Data", use_container_width=True):
        from generate_samples import SAMPLE_RESUMES
        st.session_state.parsed_resumes = []
        for filename, content in SAMPLE_RESUMES.items():
            parsed = {
                'filename': filename,
                'raw_text': content,
                'clean_text': clean_text(content),
                'name': content.strip().split('\n')[0],
                'email': [l for l in content.split('\n') if '@' in l],
                'phone': '',
                'char_count': len(content),
                'word_count': len(content.split())
            }
            # Fix email extraction
            import re
            em = re.search(r'[\w.]+@[\w.]+', content)
            parsed['email'] = em.group(0) if em else 'N/A'
            ph = re.search(r'\+[\d\-\s]{10,}', content)
            parsed['phone'] = ph.group(0).strip() if ph else 'N/A'

            clf = classify_resume(content)
            parsed['predicted_category'] = clf['predicted_category']
            parsed['confidence_scores']  = clf['confidence_scores']
            st.session_state.parsed_resumes.append(parsed)
            st.session_state.classified.append(parsed)
        st.success(f"✅ {len(SAMPLE_RESUMES)} demo resumes loaded!")

    st.markdown(f"""
    <div style='margin-top:20px; font-size:0.78rem; color:#4a5568;'>
        Resumes loaded: <b style='color:#00d4aa'>{len(st.session_state.parsed_resumes)}</b><br>
        Results ready: <b style='color:#00d4aa'>{len(st.session_state.match_results)}</b>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.markdown("## 🤖 AI-Based Resume Screening System")
    st.markdown("<div style='color:#8892b0; margin-bottom:24px;'>Automated candidate ranking powered by NLP · TF-IDF · Skill Matching</div>", unsafe_allow_html=True)

    results = st.session_state.match_results
    resumes = st.session_state.parsed_resumes

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    shortlisted = sum(1 for r in results if '✅' in r.get('status',''))
    avg_score   = round(sum(r['final_match_pct'] for r in results)/len(results), 1) if results else 0

    with c1:
        st.markdown(f"<div class='metric-card'><div class='metric-number'>{len(resumes)}</div><div class='metric-label'>Resumes Uploaded</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><div class='metric-number'>{len(results)}</div><div class='metric-label'>Matches Computed</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><div class='metric-number'>{shortlisted}</div><div class='metric-label'>Shortlisted</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-card'><div class='metric-number'>{avg_score}%</div><div class='metric-label'>Avg Match Score</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Quick leaderboard
    if results:
        st.markdown("### 🏆 Top Candidates")
        top3 = results[:3]
        cols = st.columns(len(top3))
        medals = ["🥇", "🥈", "🥉"]
        for i, (col, res) in enumerate(zip(cols, top3)):
            score = res['final_match_pct']
            color = "#00d4aa" if score >= 60 else "#f39c12" if score >= 40 else "#e74c3c"
            with col:
                st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size:2rem;'>{medals[i]}</div>
                    <div style='font-weight:600; color:#ccd6f6; margin:8px 0 4px;'>{res['resume_name']}</div>
                    <div style='font-size:1.8rem; font-weight:700; color:{color};'>{score}%</div>
                    <div style='font-size:0.78rem; color:#8892b0; margin-top:4px;'>{res['job_title']}</div>
                    <div style='margin-top:8px;'>{'<span class="badge-green">Shortlisted</span>' if '✅' in res['status'] else '<span class="badge-red">Rejected</span>'}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("👈 Load demo data from sidebar or upload resumes to get started.")

    # How it works
    st.markdown("---")
    st.markdown("### ⚙️ How It Works")
    steps = [
        ("📤", "Upload Resumes", "Upload PDF, DOCX, or TXT resume files"),
        ("🔍", "NLP Parsing", "Extracts text, cleans it, identifies skills"),
        ("🎯", "Job Matching", "TF-IDF + Skill Overlap scoring"),
        ("📊", "Ranking", "Candidates ranked by final match %"),
        ("💡", "Skill Advice", "Gap analysis + learning recommendations"),
    ]
    cols = st.columns(5)
    for col, (icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style='text-align:center; padding:16px; background:#1e2130; border-radius:10px; border:1px solid #2d3250;'>
                <div style='font-size:1.6rem;'>{icon}</div>
                <div style='font-weight:600; color:#ccd6f6; font-size:0.9rem; margin:8px 0 4px;'>{title}</div>
                <div style='font-size:0.75rem; color:#8892b0;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: UPLOAD RESUMES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📤 Upload Resumes":
    st.markdown("## 📤 Upload Resumes")
    st.markdown("<div style='color:#8892b0; margin-bottom:20px;'>Supports PDF, DOCX, and TXT files</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drag & drop resumes here",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True
    )

    if uploaded:
        if st.button("🚀 Parse All Resumes", use_container_width=True):
            st.session_state.parsed_resumes = []
            st.session_state.classified = []
            prog = st.progress(0)
            status_box = st.empty()

            for i, f in enumerate(uploaded):
                status_box.info(f"Parsing: {f.name} …")
                parsed = parse_resume(f, f.name)
                clf = classify_resume(parsed['clean_text'])
                parsed['predicted_category'] = clf['predicted_category']
                parsed['confidence_scores']  = clf['confidence_scores']
                st.session_state.parsed_resumes.append(parsed)
                st.session_state.classified.append(parsed)
                prog.progress((i+1)/len(uploaded))

            status_box.success(f"✅ Successfully parsed {len(uploaded)} resumes!")

    # Show parsed resumes table
    if st.session_state.parsed_resumes:
        st.markdown("---")
        st.markdown("### 📋 Parsed Resumes")
        for r in st.session_state.parsed_resumes:
            with st.expander(f"📄 {r['name']} — {r['filename']}"):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Category", r.get('predicted_category', 'N/A'))
                c2.metric("Words", r['word_count'])
                c3.metric("Email", r.get('email', 'N/A'))
                c4.metric("Phone", r.get('phone', 'N/A'))
                st.text_area("Extracted Text (preview)", r['raw_text'][:600] + "…", height=150)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MATCH & RANK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎯 Match & Rank":
    st.markdown("## 🎯 Match & Rank Candidates")

    if not st.session_state.parsed_resumes:
        st.warning("Please upload resumes or load demo data first.")
        st.stop()

    jobs = get_all_jobs()
    job_options = {f"{j['id']} — {j['title']} @ {j['company']}": j['id'] for j in jobs}

    selected_label = st.selectbox("Select a Job Description", list(job_options.keys()))
    selected_id    = job_options[selected_label]
    selected_job   = get_job_by_id(selected_id)

    # Show job details
    with st.expander("📋 View Job Description"):
        c1, c2 = st.columns([2,1])
        with c1:
            st.markdown(f"**{selected_job['title']}** at *{selected_job['company']}*")
            st.markdown(selected_job['description'])
        with c2:
            st.markdown("**Required Skills:**")
            skills_html = "".join(f"<span class='skill-pill'>{s}</span>" for s in selected_job['required_skills'])
            st.markdown(skills_html, unsafe_allow_html=True)

    # Match button
    if st.button("⚡ Run Matching Algorithm", use_container_width=True):
        with st.spinner("Computing similarity scores…"):
            results = rank_candidates(st.session_state.parsed_resumes, selected_job)
            st.session_state.match_results   = results
            st.session_state.selected_job_id = selected_id
        st.success("✅ Matching complete!")

    # Show results
    if st.session_state.match_results and st.session_state.selected_job_id == selected_id:
        results = st.session_state.match_results
        st.markdown("---")

        # Summary metrics
        shortlisted = sum(1 for r in results if '✅' in r['status'])
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Candidates", len(results))
        c2.metric("Shortlisted ✅", shortlisted)
        c3.metric("Top Score", f"{results[0]['final_match_pct']}%")

        # Chart
        st.plotly_chart(plot_match_scores(results), use_container_width=True)

        # Detailed table
        st.markdown("### 📋 Ranked Candidate List")
        for r in results:
            score = r['final_match_pct']
            if   score >= 60: score_cls, bar_color = "score-high",   "#00d4aa"
            elif score >= 40: score_cls, bar_color = "score-medium",  "#f39c12"
            else:             score_cls, bar_color = "score-low",     "#e74c3c"

            medal = {1:"🥇", 2:"🥈", 3:"🥉"}.get(r['rank'], f"#{r['rank']}")

            with st.expander(f"{medal} {r['resume_name']}  —  {score}%  {r['status']}"):
                left, right = st.columns([3,2])

                with left:
                    # Score bars
                    for label, val in [
                        ("TF-IDF Similarity", r['tfidf_score']),
                        ("Skill Overlap",      r['skill_overlap_score']),
                        ("Keyword Match",      r['keyword_score']),
                    ]:
                        st.markdown(f"<div style='font-size:0.82rem; color:#8892b0; margin-top:6px;'>{label}: <b style='color:#ccd6f6;'>{val}%</b></div>", unsafe_allow_html=True)
                        pct = min(val, 100)
                        st.markdown(f"<div class='prog-bar-bg'><div class='prog-bar-fill' style='width:{pct}%;'></div></div>", unsafe_allow_html=True)

                    st.markdown(f"<div style='margin-top:10px; font-size:0.85rem;'>📧 {r['email']} &nbsp;|&nbsp; 📞 {r['phone']}</div>", unsafe_allow_html=True)

                with right:
                    st.markdown("<div class='section-title'>✅ Matched Skills</div>", unsafe_allow_html=True)
                    if r['matched_skills']:
                        pills = "".join(f"<span class='skill-pill'>{s}</span>" for s in r['matched_skills'])
                        st.markdown(pills, unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color:#8892b0; font-size:0.8rem;'>None matched</span>", unsafe_allow_html=True)

                    st.markdown("<div class='section-title' style='margin-top:12px;'>❌ Missing Skills</div>", unsafe_allow_html=True)
                    if r['missing_skills']:
                        pills = "".join(f"<span class='skill-pill-miss'>{s}</span>" for s in r['missing_skills'][:6])
                        st.markdown(pills, unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color:#00d4aa; font-size:0.8rem;'>All skills matched! 🎉</span>", unsafe_allow_html=True)

        # Export CSV
        st.markdown("---")
        df = pd.DataFrame([{
            'Rank': r['rank'], 'Name': r['resume_name'],
            'Match %': r['final_match_pct'], 'Status': r['status'],
            'Matched Skills': ', '.join(r['matched_skills']),
            'Missing Skills': ', '.join(r['missing_skills']),
            'Email': r['email']
        } for r in results])
        st.download_button("⬇️ Download Results CSV", df.to_csv(index=False),
                           "ranked_candidates.csv", "text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Analytics":
    st.markdown("## 📊 Analytics Dashboard")

    results  = st.session_state.match_results
    resumes  = st.session_state.parsed_resumes
    classify = st.session_state.classified

    if not results and not resumes:
        st.info("Load demo data or run matching first to see analytics.")
        st.stop()

    r1, r2 = st.columns(2)

    with r1:
        if results:
            st.plotly_chart(plot_shortlist_pie(results), use_container_width=True)

    with r2:
        if classify:
            st.plotly_chart(plot_category_distribution(classify), use_container_width=True)

    if results:
        st.plotly_chart(plot_match_scores(results), use_container_width=True)
        st.plotly_chart(plot_skill_demand(results), use_container_width=True)

        # Score breakdown per candidate
        st.markdown("### 🔬 Score Breakdown Per Candidate")
        names = [r['resume_name'] for r in results]
        sel   = st.selectbox("Select candidate", names)
        sel_r = next(r for r in results if r['resume_name'] == sel)
        st.plotly_chart(plot_score_breakdown(sel_r), use_container_width=True)

    # Category stats table
    if classify:
        st.markdown("### 📁 Resume Category Breakdown")
        cat_df = pd.DataFrame([{
            'Name': r['name'],
            'Category': r.get('predicted_category', 'N/A'),
            'IT %': r.get('confidence_scores', {}).get('IT', 0),
            'Marketing %': r.get('confidence_scores', {}).get('Marketing', 0),
            'Finance %': r.get('confidence_scores', {}).get('Finance', 0),
            'Engineering %': r.get('confidence_scores', {}).get('Engineering', 0),
        } for r in classify])
        st.dataframe(cat_df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SKILL ADVISOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Skill Advisor":
    st.markdown("## 💡 Skill Gap Advisor")
    st.markdown("<div style='color:#8892b0; margin-bottom:20px;'>Get personalised skill recommendations for each candidate</div>", unsafe_allow_html=True)

    results = st.session_state.match_results
    if not results:
        st.warning("Run the Match & Rank step first.")
        st.stop()

    names  = [r['resume_name'] for r in results]
    chosen = st.selectbox("Choose Candidate", names)
    r = next(x for x in results if x['resume_name'] == chosen)

    advice = get_skill_gap_recommendations(r['matched_skills'], r['missing_skills'], '')

    col1, col2 = st.columns(2)

    with col1:
        score = r['final_match_pct']
        color = "#00d4aa" if score >= 60 else "#f39c12" if score >= 40 else "#e74c3c"
        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size:0.9rem; color:#8892b0; margin-bottom:8px;'>Overall Match Score</div>
            <div style='font-size:3rem; font-weight:700; color:{color};'>{score}%</div>
            <div style='margin-top:8px;'>{'<span class="badge-green">✅ Shortlisted</span>' if score >= 40 else '<span class="badge-red">❌ Rejected</span>'}</div>
        </div>
        <div class='metric-card' style='margin-top:12px;'>
            <div style='font-size:0.9rem; color:#8892b0;'>Strength Level</div>
            <div style='font-size:1.5rem; font-weight:700; color:#ccd6f6; margin-top:4px;'>{advice['strength_level']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        m1, m2 = st.columns(2)
        m1.metric("✅ Skills Matched", advice['matched_count'])
        m2.metric("❌ Skills Missing", advice['missing_count'])
        st.markdown(f"<div style='color:#8892b0; font-size:0.85rem; margin-top:8px;'>{advice['summary']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-title'>✅ Skills You Have</div>", unsafe_allow_html=True)
        if r['matched_skills']:
            pills = "".join(f"<span class='skill-pill'>{s}</span>" for s in r['matched_skills'])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("No skills matched.")

    with c2:
        st.markdown("<div class='section-title'>📚 Skills to Learn</div>", unsafe_allow_html=True)
        for rec in advice['top_recommendations']:
            st.markdown(f"""
            <div style='background:#1a1e2e; border:1px solid #2d3250; border-radius:8px;
                        padding:10px 14px; margin-bottom:8px;'>
                <span class='skill-pill-miss'>{rec['skill']}</span>
                <div style='font-size:0.78rem; color:#8892b0; margin-top:6px;'>📎 {rec['resource']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Better job matches
    st.markdown("---")
    st.markdown("<div class='section-title'>🔗 Better Job Matches</div>", unsafe_allow_html=True)
    all_jobs = get_all_jobs()
    better = []
    for job in all_jobs:
        res = match_resume_to_job(
            next(x for x in st.session_state.parsed_resumes if x['name'] == chosen),
            job
        )
        better.append((job['title'], job['company'], res['final_match_pct']))
    better.sort(key=lambda x: x[2], reverse=True)
    for title, company, sc in better:
        bar_w = min(sc, 100)
        color  = "#00d4aa" if sc >= 60 else "#f39c12" if sc >= 40 else "#e74c3c"
        st.markdown(f"""
        <div style='background:#1a1e2e; border:1px solid #2d3250; border-radius:8px;
                    padding:12px 16px; margin-bottom:8px; display:flex; align-items:center; gap:16px;'>
            <div style='flex:1;'>
                <div style='font-weight:600; color:#ccd6f6;'>{title}</div>
                <div style='font-size:0.78rem; color:#8892b0;'>{company}</div>
                <div class='prog-bar-bg' style='margin-top:6px;'>
                    <div class='prog-bar-fill' style='width:{bar_w}%; background:{color};'></div>
                </div>
            </div>
            <div style='font-size:1.4rem; font-weight:700; color:{color}; min-width:52px; text-align:right;'>{sc}%</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HR CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧠 HR Chatbot":
    st.markdown("## 🧠 HR AI Chatbot")
    st.markdown("<div style='color:#8892b0; margin-bottom:20px;'>Ask anything about candidates, job matches, or hiring advice</div>", unsafe_allow_html=True)

    # Build system context from session state
    results = st.session_state.match_results
    resumes = st.session_state.parsed_resumes

    context_parts = ["You are an expert HR assistant for TEYZIX CORE. You help with resume screening, candidate ranking, and hiring decisions. Be concise, professional, and data-driven."]

    if results:
        context_parts.append(f"\nCurrent job: {results[0]['job_title']}")
        context_parts.append(f"Total candidates: {len(results)}")
        context_parts.append(f"Shortlisted: {sum(1 for r in results if '✅' in r['status'])}")
        top = results[0]
        context_parts.append(f"Top candidate: {top['resume_name']} with {top['final_match_pct']}% match")
        for r in results:
            context_parts.append(
                f"- {r['resume_name']}: {r['final_match_pct']}% match, "
                f"matched skills: {', '.join(r['matched_skills'][:5])}, "
                f"missing: {', '.join(r['missing_skills'][:3])}"
            )

    if resumes:
        context_parts.append(f"\nUploaded resumes: {', '.join(r['name'] for r in resumes)}")

    system_prompt = "\n".join(context_parts)

    # Suggested questions
    st.markdown("**💬 Try asking:**")
    suggestions = [
        "Who is the best candidate?",
        "What skills are most in demand?",
        "Which candidates should I interview?",
        "How can I improve our job description?",
        "What are the top missing skills?"
    ]
    cols = st.columns(len(suggestions))
    for col, q in zip(cols, suggestions):
        if col.button(q, use_container_width=True):
            st.session_state.setdefault('chat_history', [])
            st.session_state['chat_history'].append({"role": "user", "content": q})

    st.markdown("---")

    # Chat history display
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    for msg in st.session_state['chat_history']:
        role  = msg['role']
        icon  = "🧑" if role == "user" else "🤖"
        align = "right" if role == "user" else "left"
        bg    = "#1a2744" if role == "user" else "#1e2130"
        st.markdown(f"""
        <div style='display:flex; justify-content:{"flex-end" if role=="user" else "flex-start"}; margin:8px 0;'>
            <div style='background:{bg}; border-radius:12px; padding:10px 16px;
                        max-width:75%; font-size:0.9rem; color:#ccd6f6; border:1px solid #2d3250;'>
                <b>{icon}</b> {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Ask about candidates, skills, or hiring…")

    if user_input:
        st.session_state['chat_history'].append({"role": "user", "content": user_input})

        # Call Anthropic API
        with st.spinner("Thinking…"):
            try:
                import requests
                messages = [{"role": m["role"], "content": m["content"]}
                            for m in st.session_state['chat_history']]

                resp = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "claude-sonnet-4-6",
                        "max_tokens": 1000,
                        "system": system_prompt,
                        "messages": messages
                    },
                    timeout=30
                )
                data = resp.json()
                reply = data['content'][0]['text'] if data.get('content') else "Sorry, I couldn't get a response."
            except Exception as e:
                reply = f"Error connecting to AI: {str(e)}"

        st.session_state['chat_history'].append({"role": "assistant", "content": reply})
        st.rerun()
