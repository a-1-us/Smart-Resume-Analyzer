import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pdfminer.high_level import extract_text

# Folder containing resumes
resume_folder = r"C:\Users\tanus\OneDrive\Desktop\Resume Analyzer\Uploaded_Resume"

stop_words = set(stopwords.words('english'))

SKILL_KEYWORDS = {
    'python', 'java', 'sql', 'machine', 'learning', 'nlp',
    'deep', 'excel', 'power', 'bi', 'tableau',
    'html', 'css', 'javascript', 'react'
}

def extract_email(text):
    match = re.findall(r'\S+@\S+', text)
    return match[0] if match else ''

def extract_phone(text):
    match = re.findall(r'\+?\d[\d\s-]{7,}\d', text)
    return match[0] if match else ''

def extract_skills_nlp(text):
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w.isalpha() and w not in stop_words]
    skills_found = set(tokens) & SKILL_KEYWORDS
    return ", ".join(sorted(skills_found))

data_list = []

for file in os.listdir(resume_folder):
    if file.lower().endswith(".pdf"):
        path = os.path.join(resume_folder, file)
        print("Processing:", file)

        text = extract_text(path)
        name = os.path.splitext(file)[0]

        data_list.append({
            "Name": name,
            "Email": extract_email(text),
            "Phone": extract_phone(text),
            "Skills": extract_skills_nlp(text),
            "Resume": text
        })

df = pd.DataFrame(data_list)
csv_path = os.path.join(resume_folder, "classmates_resume_data.csv")
df.to_csv(csv_path, index=False)

print("✅ CSV saved at:", csv_path)
