import os
import pandas as pd
from text_extractor import extract_text
from ranking_engine import clean_text, extract_keywords, match_keywords, compute_similarity
from spacy.lang.en.stop_words import STOP_WORDS

# Define additional domain-specific generic words to ignore
DOMAIN_STOPWORDS = {
    "company", "organization", "corporation", "work", "employee", "job", "position",
    "skills", "team", "experience", "role", "person", "description", "project"
}

def rank_resumes(jd_text, folder_path):
    print("✅ rank_resumes() function called")
    print("📝 JD sample:", jd_text[:100])
    print("📂 Resume folder path:", folder_path)

    resumes = []
    jd_keywords = extract_keywords(clean_text(jd_text))

    # Filter JD keywords to remove generic or stop words
    important_keywords = [kw for kw in jd_keywords
                          if kw.lower() not in STOP_WORDS
                          and kw.lower() not in DOMAIN_STOPWORDS
                          and len(kw) > 3]
    print("🎯 Filtered JD keywords:", important_keywords)

    for file_name in os.listdir(folder_path):
        if not file_name.lower().endswith((".pdf", ".docx")):
            continue

        file_path = os.path.join(folder_path, file_name)
        print("🔍 Reading file:", file_name)

        resume_text = extract_text(file_path)
        print("📄 Resume text length:", len(resume_text))

        cleaned_resume = clean_text(resume_text)
        score = compute_similarity(jd_text, resume_text)
        matched, accuracy = match_keywords(resume_text, important_keywords)

        # Normalize and adjust final score (accuracy weighted more)
        norm_score = (score - 0.5) / (1 - 0.5)
        norm_score = max(0, min(1, norm_score))
        boost = 0.05 if len(matched) >= 5 else 0
        final_score = round((0.2 * norm_score) + (0.8 * accuracy) + boost, 4)

        resumes.append({
            "Filename": file_name,
            "Score": round(score, 2),
            "Accuracy": round(accuracy, 2),
            "Final_Score": final_score
        })

    df = pd.DataFrame(resumes)
    print("📈 Final DataFrame shape:", df.shape)
    print(df.head())

    df = df.sort_values(by="Final_Score", ascending=False)
    df.to_csv("ranked_uploaded_resumes.csv", index=False)
    return df