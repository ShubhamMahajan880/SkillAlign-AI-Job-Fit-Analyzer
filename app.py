import streamlit as st
import pandas as pd

from src.resume_parser import extract_resume_text, extract_skills
from src.jd_parser import extract_jd_skills
from src.matcher import calculate_match_details
from src.eligibility import eligibility_status
from src.suggestions import learning_recommendations

SKILLS = [
    "python", "java", "sql", "html", "css", "javascript",
    "react", "node", "docker", "git",
    "data structures", "algorithms", "machine learning",
    "api", "rest"
]

st.set_page_config(
    page_title="AI Resume & Job Matcher",
    layout="centered"
)

# ---------- Subtle Background Watermark ----------
st.markdown(
    """
    <style>
    .watermark {
        position: fixed;
        bottom: 12px;
        right: 12px;
        opacity: 0.15;
        font-size: 12px;
        color: black;
        z-index: 1000;
    }
    </style>
    <div class="watermark">Shubham Mahajan</div>
    """,
    unsafe_allow_html=True
)

# ---------- Header ----------
st.title("AI-Powered Resume & Job Matcher")
st.caption("Created by Shubham Mahajan")

st.progress(0)

# ---------- STEP 1 ----------
st.header("Step 1: Upload Resume")
resume_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)

progress = st.progress(0)

if resume_file:
    progress.progress(25)
    st.success("Resume uploaded successfully.")

    # ---------- STEP 2 ----------
    st.header("Step 2: Paste Job Description")
    jd_text = st.text_area(
        "Paste the complete job description here"
    )

    if jd_text.strip():
        progress.progress(50)
        st.info("Analyzing resume and job description...")

        # Resume processing
        resume_text = extract_resume_text(resume_file)
        resume_skills = extract_skills(resume_text, SKILLS)

        # JD processing
        jd_skills = extract_jd_skills(jd_text, SKILLS)

        progress.progress(75)

        # Matching
        result = calculate_match_details(resume_skills, jd_skills)

        match_percentage = result["match_percentage"]
        matched_skills = result["matched_skills"]
        missing_skills = result["missing_skills"]

        status = eligibility_status(match_percentage)

        progress.progress(100)
        st.divider()

        # ---------- RESULTS ----------
        st.header("Match Evaluation Result")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Match Percentage", f"{match_percentage}%")
        with col2:
            st.metric("Eligibility Status", status)

        # ---------- CRITERIA ----------
        st.subheader("Skill-Based Evaluation Criteria")

        criteria_df = pd.DataFrame({
            "Job Required Skills": jd_skills
        })
        st.table(criteria_df)

        # ---------- MATCHED ----------
        st.subheader("✅ Matching Criteria (You Qualify For)")
        if matched_skills:
            for skill in matched_skills:
                st.write(f"- {skill}")
        else:
            st.write("No matching criteria satisfied.")

        # ---------- MISSING ----------
        st.subheader("❌ Missing Criteria (Required for This Role)")
        if missing_skills:
            for skill in missing_skills:
                st.write(f"- {skill}")
        else:
            st.write("No missing criteria.")

        st.divider()

        # ---------- FINAL DECISION ----------
        st.subheader("Final Eligibility Explanation")

        if status == "Eligible":
            st.success(
                "You are eligible for this role based on the matching criteria above."
            )
            st.write("**Skills that qualify you for this role:**")
            for skill in matched_skills:
                st.write(f"- {skill}")
        else:
            st.warning(
                "You are not fully eligible for this role yet."
            )
            st.write("**What you should learn to qualify:**")
            recommendations = learning_recommendations(missing_skills)
            for rec in recommendations:
                st.write(f"- {rec}")

# ---------- Footer Credit ----------
st.divider()
st.markdown(
    """
    <div style="text-align: center; color: grey; font-size: 13px; padding-top: 10px;">
        Built by <b>Shubham Mahajan</b> | AI Resume & Job Matcher
    </div>
    """,
    unsafe_allow_html=True
)
