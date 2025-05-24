import streamlit as st
import fitz  # PyMuPDF
import re
import json

# Sample skills DB (you can load this from a JSON file later)
skills_db = [
    "python", "java", "sql", "excel", "communication",
    "tensorflow", "docker", "leadership", "pandas", "git"
]

st.set_page_config(page_title="Smart Resume Analyzer", layout="centered")

st.title("📄 Smart Resume Analyzer")
st.markdown("Upload your resume and paste a job description to see how well they match.")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste the Job Description here")

# Extract skills from text
def extract_skills(text, skills_db):
    text = text.lower()
    return list({skill for skill in skills_db if re.search(rf"\b{re.escape(skill)}\b", text)})

# Parse resume PDF
def parse_resume_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if uploaded_file and job_description:
    resume_text = parse_resume_text(uploaded_file)
    resume_skills = extract_skills(resume_text, skills_db)
    jd_skills = extract_skills(job_description, skills_db)

    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)
    score = round(len(matched) / len(jd_skills) * 100, 2) if jd_skills else 0

    st.success(f"✅ Match Score: {score}%")
    st.markdown("### ✅ Matched Skills")
    st.write(", ".join(matched) if matched else "None")

    st.markdown("### ❌ Missing Skills")
    st.write(", ".join(missing) if missing else "None")

    st.markdown("### 📋 All Resume Skills")
    st.write(", ".join(resume_skills))
