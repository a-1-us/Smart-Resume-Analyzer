import os
import pandas as pd
import streamlit as st
from pdfminer.high_level import extract_text

UPLOAD_FOLDER = r"C:\Users\tanus\OneDrive\Desktop\Resume Analyzer\Uploaded_Resume"
CSV_FILE = r"C:\Users\tanus\OneDrive\Desktop\classmates_resume_data.csv"

st.title("Resume Analyzer")

df = pd.read_csv(CSV_FILE)

student_name = st.selectbox("Select Student", df["Name"].tolist())
student = df[df["Name"] == student_name].iloc[0]

# ✅ CORRECT way
resume_path = os.path.join(UPLOAD_FOLDER, student["Resume_File"])

if not os.path.exists(resume_path):
    st.error("❌ Resume PDF not found")
else:
    text = extract_text(resume_path)

    st.subheader("Resume Content")
    st.text_area("Extracted Text", text, height=350)

    st.subheader("Student Details")
    st.write("📧 Email:", student["Email"])
    st.write("📞 Phone:", student["Phone"])
    st.write("🛠 Skills:", student["Skills"])
