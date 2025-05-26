import streamlit as st
from pypdf import PdfReader
import subprocess
import re

def extract_skills(text, skills_db):
    text = text.lower()
    return list({skill for skill in skills_db if re.search(rf"\b{re.escape(skill)}\b", text)})


# Skill list (expand as needed)
skills_db = [
    "python", "java", "c", "c++", "c#", "sql", "cloud",
    "docker", "security", "distributed", "communication"
]

# Extract text from resume
def extract_resume_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

def extract_skills(text, skill_db):
    text = text.lower()
    return list({skill for skill in skill_db if re.search(rf"\b{re.escape(skill)}\b", text)})

# Streamlit UI
st.title("📄 Smart Resume Analyzer")

uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste Job Description")

if uploaded_file and job_description:
    resume_text = extract_resume_text(uploaded_file)
    jd_skills = extract_skills(job_description, skills_db)
    resume_skills = extract_skills(resume_text, skills_db)

    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)
    score = round(len(matched) / len(jd_skills) * 100, 2) if jd_skills else 0

    st.success(f"🎯 Match Score: {score}%")
    st.markdown("### ✅ Matched Skills")
    st.write(", ".join(matched) if matched else "None")

    st.markdown("### ❌ Missing Skills")
    st.write(", ".join(missing) if missing else "None")

    st.markdown("### 📋 All Resume Skills")
    st.write(", ".join(resume_skills))
