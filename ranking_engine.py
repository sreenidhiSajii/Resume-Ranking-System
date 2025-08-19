import re
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_md")

def clean_text(text):
    text = re.sub(r"<.*?>", "", text)  # remove HTML tags
    text = re.sub(r"[^a-zA-Z0-9\\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def extract_keywords(text):
    tokens = re.findall(r'\b\w{4,}\b', text.lower())
    return list(set([t for t in tokens if t not in STOP_WORDS]))

def match_keywords(resume_text, jd_keywords):
    resume_tokens = set(re.findall(r'\b\w+\b', resume_text.lower()))
    matched = [kw for kw in jd_keywords if kw in resume_tokens]
    accuracy = round(len(matched) / len(jd_keywords), 2) if jd_keywords else 0
    return matched, accuracy

def highlight_keywords(text, keywords):
    for kw in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(r'\b(' + re.escape(kw) + r')\b', re.IGNORECASE)
        text = pattern.sub(r'**\1**', text)
    return text

def compute_similarity(jd_text, resume_text):
    jd_vec = nlp(jd_text).vector.reshape(1, -1)
    res_vec = nlp(resume_text).vector.reshape(1, -1)
    return cosine_similarity(jd_vec, res_vec)[0][0]
