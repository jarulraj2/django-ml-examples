import spacy
import re



# --- Name ---
def extract_name(text):
    nlp = spacy.load("en_core_web_sm")
    patterns = [
        r'(?i)\bmy name is\s+([A-Z][a-z]+(?:\s+[A-Z](?:[a-z]+)?))',
        r'(?i)\bi am\s+([A-Z][a-z]+(?:\s+[A-Z](?:[a-z]+)?))',
        r'(?i)\bmyself\s+([A-Z][a-z]+(?:\s+[A-Z](?:[a-z]+)?))',
        r'(?i)\bname\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z](?:[a-z]+)?))',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return None

# --- Email ---
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

# --- Phone ---
def extract_phone(text):
    match = re.search(r'(\+?\d{1,3}[-\s.]?)?\d{10}', text)
    return match.group(0) if match else None

# --- Job Role ---
def extract_job_role(text):
    match = re.search(r'\b(Job Role|Role|Position)\s*[:\-]?\s*(.+)', text, re.IGNORECASE)
    return match.group(2).strip() if match else None

# --- Skills ---
def extract_skills(text):
    skills_keywords = [
        "Python", "Django", "Flask", "FastAPI", "Machine Learning", "Deep Learning", 
        "NLP", "AI", "SQL", "JavaScript", "HTML", "CSS", "React", "Linux", "Docker"
    ]
    lower_text = text.lower()
    return list(set([skill for skill in skills_keywords if skill.lower() in lower_text]))

# --- Education ---
def extract_education(text):
    matches = re.findall(
        r'((B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|B\.?E|M\.?E|B\.?C\.?A|M\.?C\.?A).+?\d{4})',
        text, re.IGNORECASE
    )
    return [edu[0].strip() for edu in matches]

# --- Experience ---



import re

def extract_experience(text):
    patterns = [
        # Strictest and longest pattern first
        r'(?:worked|joined|employed)\s+(?:as\s+)?([A-Za-z\s]+?)\s+(?:at|in)\s+([A-Za-z\s]+?)\s+from\s+(\d{4})\s+to\s+(\d{4}|present|now)',
        r'([A-Za-z\s]+?)\s+at\s+([A-Za-z\s]+?)\s+\((\d{4})\s*[-–]\s*(\d{4}|present|now)\)',
        r'([A-Za-z\s]+?)\s+at\s+([A-Za-z\s]+?)\s+from\s+(\d{4})\s+to\s+(\d{4}|present|now)',
        r'(?:worked|joined|employed)\s+(?:as\s+)?([A-Za-z\s]+?)\s+(?:at|in)\s+([A-Za-z\s]+?)\s+in\s+(\d{4})',
    ]

    experience = []
    seen = set()
    matched_spans = []

    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            span = match.span()
            # Skip if it overlaps any previous match
            if any(start <= span[0] < end or start < span[1] <= end for start, end in matched_spans):
                continue
            matched_spans.append(span)

            groups = match.groups()
            if len(groups) == 4:
                position, company, from_year, to_year = groups
            elif len(groups) == 3:
                position, company, from_year = groups
                to_year = "Present"
            else:
                continue

            key = f"{position.strip().lower()}|{company.strip().lower()}|{from_year}|{to_year.lower()}"
            if key in seen:
                continue
            seen.add(key)

            experience.append({
                "position": position.strip().title(),
                "company": company.strip().title(),
                "from": from_year,
                "to": to_year.title() if to_year.lower() in ["present", "now"] else to_year
            })

    return experience





# --- Projects ---
def extract_projects(text):
    projects = []
    for line in text.split('\n'):
        if 'project' in line.lower() or any(kw in line.lower() for kw in ['system', 'app', 'website']):
            projects.append(line.strip())
    return projects


def extract_certificates(text):
    lines = text.split('\n')
    cert_lines = []
    capturing = False

    for line in lines:
        line = line.strip()
        if line.lower().startswith("certificates:"):
            capturing = True
            continue
        elif capturing:
            if not line:  # stop if blank line
                break
            cert_lines.append(line)
    
    return cert_lines


# --- Master Extractor ---
def extract_resume_data(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "job_role": extract_job_role(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certificates": extract_certificates(text),
    }
