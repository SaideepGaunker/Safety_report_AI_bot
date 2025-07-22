# 🚨 Safety Report AI Bot (Backend)

> ⚠️ **Note:** All sensitive information such as API keys, email credentials, and personal details have been removed from this repository for security purposes. Please configure your own credentials in a `.env` file or environment variables before running the project.

---

## 📌 Project Overview

This backend is part of a community safety reporting system powered by AI. It is designed to:

- Receive safety incident reports from a frontend chatbot interface (built in **Botpress**)
- Generate a brief **technical summary** of the report using **Google Gemini API**
- Log the data into a **CSV file**
- Send a **summary email** notification to the concerned department or team

---

🚀 Features
💬 Interactive chatbot built using Botpress
⚙️ Backend developed using FastAPI
🤖 AI-powered summaries using Gemini (Google AI Studio)
📊 Logging system via Google Sheets
📧 Automated email alerts using SMTP
☁️ Deployed using Railway for public access

## ⚙️ Tech Stack

- 🐍 **Python 3.10+**
- 🚀 **FastAPI** – for backend API development
- 🧠 **Google Gemini API** – for intelligent summarization
- 📧 **SMTP (Gmail)** – for email notifications
- 🗃️ **CSV** – to log reports locally
- 🌐 **Railway** – for backend deployment (or use any preferred cloud service)

---

## 🧾 How It Works

1. The frontend bot collects:
   - 📍 Incident location  
   - 🚨 Type of issue  
   - 📝 Description of the problem

2. The backend receives this data via POST `/report`

3. It generates a professional summary using Gemini API

4. Logs the complete data in `reports.csv`

5. Sends an email summary to a pre-defined recipient (e.g., safety department)

---


