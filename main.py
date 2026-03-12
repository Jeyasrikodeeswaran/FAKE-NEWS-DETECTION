import requests
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

class EmailInput(BaseModel):
    email_text: str
    sender_email: str
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailInput(BaseModel):
    email_text: str
    sender_email: str


def extract_details(email_text):
    # simple rule based extraction
    name = None
    company = None

    if "Google" in email_text:
        company = "Google"

    if "Microsoft" in email_text:
        company = "Microsoft"

    if "HR" in email_text:
        name = "HR Manager"

    return name, company

def check_domain(domain, company):

    official_domains = {
        "Google": "google.com",
        "Microsoft": "microsoft.com",
        "Amazon": "amazon.com",
        "Infosys": "infosys.com"
    }

    if company in official_domains:
        if official_domains[company] in domain:
            return "Verified company domain"
        else:
            return "Suspicious domain"

    return "Domain not detected"

@app.post("/analyze")
def analyze_email(data: EmailInput):
    sender_email = data.sender_email

    domain = sender_email.split("@")[-1]

    email_text = data.email_text

    name, company = extract_details(email_text)

    domain_check = check_domain(domain, company)
    
    linkedin_check = linkedin_verification(company)

    red_flags = detect_red_flags(email_text)

    explanation = generate_explanation(domain_check, red_flags)

    recommendation = "Avoid sending personal information or payments. Verify the opportunity through the official company website."

    score, level = risk_score(domain_check, linkedin_check)


    return {
        "person": name,
        "company": company,
        "domain_check": domain_check,
        "linkedin_check": linkedin_check,
        "risk_score": score,
        "risk_level": level,
        "red_flags": red_flags,
        "explanation": explanation,
        "recommendation": recommendation
    }

def linkedin_verification(company):

    search_query = f"https://www.google.com/search?q=site:linkedin.com/company+{company}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_query, headers=headers)

    if "linkedin.com/company" in response.text:
        return "Company found on LinkedIn"
    else:
        return "No LinkedIn presence detected"

def risk_score(domain_check, linkedin_check):

    score = 0

    if domain_check == "Suspicious domain":
        score += 50

    if linkedin_check == "No LinkedIn presence detected":
        score += 30

    if score < 30:
        level = "SAFE"
    elif score < 60:
        level = "SUSPICIOUS"
    else:
        level = "HIGH RISK"

    return score, level

def detect_red_flags(email_text):

    flags = []

    keywords = [
        "registration fee",
        "pay",
        "urgent",
        "limited seats",
        "bank details",
        "aadhaar",
        "payment",
        "security deposit"
    ]

    for word in keywords:
        if word.lower() in email_text.lower():
            flags.append(word)

    return flags

def generate_explanation(domain_check, flags):

    if domain_check == "Suspicious domain":
        return "The email claims to be from a company but uses a free email provider."

    if len(flags) > 0:
        return "The email contains suspicious phrases commonly used in scams."

    return "No major red flags detected."

def generate_explanation(domain_check, red_flags):

    if domain_check == "Suspicious domain":
        return "The email claims to be from a company but uses a free email provider."

    if len(red_flags) > 0:
        return "The email contains suspicious phrases commonly used in scams."

    return "No major red flags detected."