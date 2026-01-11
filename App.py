import streamlit as st
import pandas as pd
import os
import re
import nltk
from pdfminer.high_level import extract_text

# Download NLTK stopwords
nltk.download("stopwords")
from nltk.corpus import stopwords

# ---------- CONFIG ----------
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")
st.title("Smart Resume Analyzer")

# ---------- UPLOAD FOLDER ----------
UPLOAD_FOLDER = r"C:\Users\tanus\OneDrive\Desktop\Resume Analyzer\Uploaded_Resume"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- MENU ----------
menu = ["Upload Resumes (PDFs)", "Analyze Resume", "Admin"]
choice = st.sidebar.selectbox("Select Option", menu)

# ---------- FUNCTIONS ----------
def clean_resume_text(text):
    """Clean resume text"""
    text = text.replace("•", "\n• ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\+?\d[\d\s]{8,}', '', text)
    return text.strip()

def extract_email(text):
    match = re.findall(r'\S+@\S+', text)
    return match[0] if match else ''

def extract_phone(text):
    match = re.findall(r'\+?\d[\d\s-]{7,}\d', text)
    return match[0] if match else ''

def extract_skills_nltk(text):
    skill_keywords = [
        'Python', 'SQL', 'Excel', 'Machine Learning', 'NLP', 'Deep Learning',
        'Java', 'C++', 'HTML', 'CSS', 'JavaScript', 'React', 'Tableau', 'Power BI'
    ]
    text_tokens = [word for word in re.split(r'\W+', text.lower()) if word and word not in stopwords.words('english')]
    skills_found = [skill for skill in skill_keywords if skill.lower() in text_tokens]
    return skills_found

# ---------- UPLOAD RESUMES ----------
if choice == "Upload Resumes (PDFs)":
    st.subheader("Upload PDF Resumes")
    uploaded_files = st.file_uploader("Drag & Drop PDFs here", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        data_list = []
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_FOLDER, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            st.success(f"Uploaded: {file.name}")

            try:
                text = extract_text(file_path)
                name = os.path.splitext(file.name)[0]
                email = extract_email(text)
                phone = extract_phone(text)
                skills = extract_skills_nltk(text)

                data_list.append({
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Skills": ", ".join(skills),
                    "Resume_File": file.name
                })
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

        if data_list:
            df = pd.DataFrame(data_list)
            csv_path = os.path.join(UPLOAD_FOLDER, "classmates_resume_data.csv")
            df.to_csv(csv_path, index=False)
            st.success(f"✅ All resume details extracted!\nCSV saved at: {csv_path}")

# ---------- ANALYZE RESUME ----------
elif choice == "Analyze Resume":
    st.subheader("Analyze Student Resume")

    csv_path = os.path.join(UPLOAD_FOLDER, "classmates_resume_data.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        student_name = st.selectbox("Select Student", df["Name"].tolist())
        student = df[df["Name"] == student_name].iloc[0]

        resume_path = os.path.join(UPLOAD_FOLDER, student["Resume_File"])
        if os.path.exists(resume_path):
            resume_text = extract_text(resume_path)
            cleaned_text = clean_resume_text(resume_text)
            st.markdown("### Cleaned Resume Content")
            st.text_area("Resume Text", cleaned_text, height=350)

            skills = extract_skills_nltk(cleaned_text)
            st.markdown("##  Skills Found ")
            st.write(skills)
            st.bar_chart(pd.Series(skills).value_counts())

        st.markdown("## Resume Details")
        for col in df.columns:
            if col != "Resume_File":
                st.markdown(f"**{col}:** {student[col]}")

    else:
        st.warning("No CSV found. Please upload PDFs first.")

# ---------- ADMIN PANEL ----------
else:
    st.subheader("Admin Panel")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "Tanu" and password == "1234":
            st.success("Welcome Admin")
            files = os.listdir(UPLOAD_FOLDER)
            total_students = 0

            st.markdown("### Uploaded Files")
            for file in files:
                if file.endswith(".pdf") or file.endswith(".csv"):
                    st.write(file)
                    if file.endswith(".csv"):
                        df = pd.read_csv(os.path.join(UPLOAD_FOLDER, file))
                        total_students += len(df)

            st.markdown("---")
            st.write("Total CSV Files:", len([f for f in files if f.endswith(".csv")]))
            st.write("Total Resumes (Students):", total_students)
        else:
            st.error("Invalid Credentials")
