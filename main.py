from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import csv
import os


app = FastAPI()

# ✅ Correct CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cdn.botpress.cloud"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Config 
GEMINI_API_KEY = "" 
EMAIL_SENDER = "example@gmail.com"
EMAIL_PASSWORD = "password"
EMAIL_RECEIVER = "example@gmail.com"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

class Report(BaseModel):
    location: str
    issue_type: str
    issue_desc: str

def generate_summary(location, issue_type, issue_desc):
    prompt = f"Summarize the following community safety issue:\nLocation: {location}\nIssue: {issue_type}\nDetails: {issue_desc}"
    response = model.generate_content(prompt)
    return response.text.strip()

def log_to_csv(location, issue_type, issue_desc, summary):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile("reports.csv")
    with open("reports.csv", "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Location", "Issue Type", "Issue Description", "Summary"])
        writer.writerow([now, location, issue_type, issue_desc, summary])

def send_email(summary, location):
    subject = f"Issue Reported in {location}"
    body = f"Summary:\n\n{summary}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

@app.post("/report")
async def receive_report(report: Report):
    summary = generate_summary(report.location, report.issue_type, report.issue_desc)
    log_to_csv(report.location, report.issue_type, report.issue_desc, summary)
    send_email(summary, report.location)
    return {"message": "Report successfully submitted", "summary": summary}
