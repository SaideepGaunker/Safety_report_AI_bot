
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import csv
import os

# -------- CONFIGURATION SECTION -------- #

# Gemini API Key (from Google AI Studio)
GEMINI_API_KEY = "AIzaSyBQn4px9zAFsw5OpmZHqHA3kdCzg2XSViM"

# Email setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "saideepcoc1@gmail.com"
EMAIL_PASSWORD = "svws opfe garj xemo"  # Use App Password, not raw Gmail password
EMAIL_RECEIVER = "saigaunker12345@gmail.com"

# --------------------------------------- #

app = FastAPI()

class Report(BaseModel):
    location: str
    issue_type: str
    issue_desc: str

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# -------- FUNCTIONS -------- #

def generate_summary(location, issue_type, issue_desc):
    prompt = f"Summarize the following community safety issue in a formal tone.\nLocation: {location}\nIssue: {issue_type}\nDetails: {issue_desc}"
    response = model.generate_content(prompt)
    return response.text.strip()

def log_to_csv(location, issue_type, issue_desc, summary):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile("reports.csv")
    with open("reports.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Location", "Issue Type", "Issue Description", "Summary"])
        writer.writerow([now, location, issue_type, issue_desc, summary])

def send_email(summary, location):
    subject = f"New Safety Issue Reported in {location}"
    body = f"A new issue was reported:\n\n{summary}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

# -------- API ENDPOINT -------- #

@app.post("/report")
async def receive_report(report: Report):
    summary = generate_summary(report.location, report.issue_type, report.issue_desc)
    log_to_csv(report.location, report.issue_type, report.issue_desc, summary)
    send_email(summary, report.location)

    return {
        "message": "Report successfully submitted",
        "summary": summary
    }
